from argparse import ArgumentError
from linebot import LineBotApi
from linebot.models import *
from google.cloud.firestore import Client
from card.cardServices import ChanceService, DestinyService
from models import *

from services import GameService, UserService
from views import ConsoleArgument, View, ViewFactory


class BaseController:
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameService=None, userService=None):
        self._db = db
        self.lineBotApi = lineBotApi
        self.gameService = GameService(db) if gameService == None else gameService
        self.userService = UserService(db) if userService == None else userService

    def recordAndReply(self, view: View):
        self.lineBotApi.reply_message(self.event.reply_token, view.message)
        self.userService.setLastMessageId(self.userId, view.messageId)

    def handleEvent(self, event):
        self.event = event
        self.userId = event.source.user_id

    def removeUserData(self):
        self.gameService.leaveGame(self.userId)
        self.userService.delete(self.userId)

    def getUserName(self, userId):
        return self.lineBotApi.get_profile(userId).display_name

class FollowController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameService=None, userService=None):
        super().__init__(lineBotApi, db, gameService, userService)

    def handleEvent(self, event):
        super().handleEvent(event)
        if isinstance(event, UnfollowEvent):
            self.removeUserData()
        elif isinstance(event, FollowEvent):
            self.recordAndReply(ViewFactory.greeting())


class DefaultController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameService=None, userService=None):
        super().__init__(lineBotApi, db, gameService, userService)

    def handleEvent(self, event):
        super().handleEvent(event)
        if isinstance(event, PostbackEvent):
            data = PostbackData.parse(event.postback.data)
            if data.type == PostbackType.CreateGame:
                gameId = self.gameService.createGame(self.userId)
                self.userService.initGameData(self.userId)
                self.recordAndReply(
                    ViewFactory.gameCreated(
                        ConsoleArgument(
                            gameId,
                            self.getUserName(self.userId),
                            UserService.initBalance)))
                return

        elif isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            if GameService.isGameId(event.message.text):
                if self.gameService.joinGame(event.message.text, self.userId):
                    self.userService.initGameData(self.userId)
                    self.recordAndReply(
                        ViewFactory.joinGameSuccess(
                            ConsoleArgument(
                                event.message.text,
                                self.getUserName(self.userId),
                                UserService.initBalance)))
                else:
                    self.recordAndReply(ViewFactory.joinGameFail())
                return

        self.recordAndReply(ViewFactory.greeting())


class GameController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameId: str, gameService=None, userService=None):
        super().__init__(lineBotApi, db, gameService, userService)
        self.gameId = gameId

    def handleEvent(self, event):
        super().handleEvent(event)
        self.responseContext = None
        self.userName = self.getUserName(self.userId)

        try:
            if isinstance(event, PostbackEvent):
                self.data = PostbackData.parse(event.postback.data)
                excution = {
                    PostbackType.Console: self.replyConsole,
                    PostbackType.LeaveConfirm: self.replyLeaveConfirm,
                    PostbackType.Leave:self.leaveGame,
                    PostbackType.Earn: self.askEarnAmount,
                    PostbackType.Pay: self.askPayAmount,
                    PostbackType.Transfer: self.askTransferTarget,
                    PostbackType.SelectTransferTarget: self.askTransferAmount,
                    PostbackType.Chance: self.drawChanceCard,
                    PostbackType.Destiny: self.drawDestinyCard,
                    PostbackType.Rollback: self.rollback,
                }

                if self.data.type in excution: excution[self.data.type]()
                return

            self.userContext = self.userService.getContext(self.userId)
            if self.userContext != None:
                excution = {
                    UserContextType.Earn: self.earn,
                    UserContextType.Pay: self.pay,
                    UserContextType.TransferAmount: self.transfer,
                }
                if self.userContext.type in excution:
                    excution[self.userContext.type]()
                return

            self.recordAndReply(ViewFactory.Console(self.getConsoleArgument()))
        finally:
            self.userService.setContext(self.userId, self.responseContext)

    def getConsoleArgument(self):
        return ConsoleArgument(
            self.gameId,
            self.userName,
            self.userService.getBalance(self.userId),
            self.gameService.getGameLogs(self.gameId))

    def replyConsole(self):
        if self.userService.isLastMessage(self.userId, self.data.messageId):
            self.recordAndReply(ViewFactory.Console(self.getConsoleArgument())) 

    def replyLeaveConfirm(self):
        self.recordAndReply(ViewFactory.leaveConfirm(self.getConsoleArgument()))

    def leaveGame(self):
        if self.userService.isLastMessage(self.userId, self.data.messageId):
            self.recordAndReply(ViewFactory.leavedGame())
            self.removeUserData()

    def askEarnAmount(self):
        self.recordAndReply(ViewFactory.askAmount(self.getConsoleArgument(), "領取"))
        self.responseContext = UserContext(UserContextType.Earn)

    def askPayAmount(self):
        self.recordAndReply(ViewFactory.askAmount(self.getConsoleArgument(), "繳交"))
        self.responseContext = UserContext(UserContextType.Pay)

    def askTransferTarget(self):
        players = {}
        for memberId in self.gameService.getOtherMembers(self.gameId, self.userId):
            players[memberId] = self.getUserName(memberId)
        if len(players) < 1:
            self.recordAndReply(ViewFactory.Console(
                self.getConsoleArgument(), text="這場遊戲還沒有其他玩家喔~\n快邀請朋友加入吧!"))
        else:
            self.recordAndReply(ViewFactory.askTransferTarget(self.getConsoleArgument(), players))

    def askTransferAmount(self):
        if self.userService.isLastMessage(self.userId, self.data.messageId):
            self.recordAndReply(ViewFactory.askAmount(self.getConsoleArgument(), f"匯給 {self.getUserName(self.data.params)} "))
            self.responseContext = UserContext(UserContextType.TransferAmount, self.data.params)

    def drawChanceCard(self):
        cardService = ChanceService(self._db)
        if self.data.params == None:
            cardViewFunc = cardService.draw(self.gameId)
            self.recordAndReply(cardViewFunc(self.getConsoleArgument()))
        elif self.userService.isLastMessage(self.userId, self.data.messageId):
            cardService.excuteCard(self)

    def drawDestinyCard(self):
        cardService = DestinyService(self._db)
        if self.data.params == None:
            cardViewFunc = cardService.draw(self.gameId)
            self.recordAndReply(cardViewFunc(self.getConsoleArgument()))
        else:
            if self.userService.isLastMessage(self.userId, self.data.messageId):
                cardService.excuteCard(self)

    def rollback(self):
        if self.userService.isLastMessage(self.userId, self.data.messageId):
            gameLog = self.gameService.getGameLog(self.gameId, self.data.params["gameLogId"])
            if not gameLog.canceled:
                if gameLog.action == GameLogAction.Transfer:
                    params = json.loads(gameLog.value)
                    self.userService.addBalance(params["from"], params["amount"])
                    self.userService.addBalance(params["to"], params["amount"] * -1)
                else:
                    self.userService.addBalance(self.userId, 
                        gameLog.value * (-1 if gameLog.action == GameLogAction.Earn else 1))
                self.gameService.rollbackGameLog(self.gameId, gameLog.id)
                self.recordAndReply(ViewFactory.Console(self.getConsoleArgument(), text="撤銷成功~"))

    def earn(self):
        try:
            if not isinstance(self.event, MessageEvent) or not isinstance(self.event.message, TextMessage):
                raise ArgumentError(None, "")
            amount = int(self.event.message.text)
            if amount <= 0:
                raise ArgumentError(None, "")
            self.userService.addBalance(self.userId, amount)
            gameLog = GameLog(self.userName, f"領取了 ${amount}", GameLogAction.Earn, amount)
            self.gameService.AddGameLog(self.gameId, gameLog)
            self.recordAndReply(ViewFactory.OperateSuccess(
                self.getConsoleArgument(), f"操作成功~\n您領取了 ${amount}", gameLog.id))
        except (ArgumentError, ValueError):
            self.recordAndReply(ViewFactory.inputError(self.getConsoleArgument()))
            self.responseContext = self.userContext

    def pay(self):
        try:
            if not isinstance(self.event, MessageEvent) or not isinstance(self.event.message, TextMessage):
                raise ArgumentError(None, "")
            amount = int(self.event.message.text)
            if amount < 1 or amount > self.userService.getBalance(self.userId):
                raise ArgumentError(None, "")
            self.userService.addBalance(self.userId, amount * -1)
            gameLog =  GameLog(self.userName, f"繳納了 ${amount}", GameLogAction.Pay, amount)
            self.gameService.AddGameLog(self.gameId, gameLog)
            self.recordAndReply(ViewFactory.OperateSuccess(
                self.getConsoleArgument(), f"操作成功~\n您繳納了 ${amount}", gameLog.id))
        except (ArgumentError, ValueError):
            self.recordAndReply(ViewFactory.inputError(self.getConsoleArgument()))
            self.responseContext = self.userContext

    def transfer(self):
        try:
            if not isinstance(self.event, MessageEvent) or not isinstance(self.event.message, TextMessage):
                raise ArgumentError(None, "")
            amount = int(self.event.message.text)
            balance = self.userService.getBalance(self.userId)
            if amount <= 0 or amount > balance:
                raise ArgumentError(None, "")
            self.userService.addBalance(self.userContext.params, amount)
            self.userService.addBalance(self.userId, amount * -1)
            toPlayerName = self.getUserName(self.userContext.params)
            gameLog = GameLog(self.userName,
                f"匯款給 {toPlayerName} ${amount}",
                GameLogAction.Transfer,
                json.dumps(
                    {"from": self.userId, "to": self.userContext.params,
                        "amount": amount},
                    separators=(',', ':')))
            self.gameService.AddGameLog(self.gameId, gameLog)
            self.recordAndReply(ViewFactory.OperateSuccess(
                self.getConsoleArgument(), f"操作成功~\n您匯了 ${amount} 給 {toPlayerName}", gameLog.id))
        except (ArgumentError, ValueError) as ex:
            self.recordAndReply(ViewFactory.inputError(self.getConsoleArgument()))
            self.responseContext = self.userContext