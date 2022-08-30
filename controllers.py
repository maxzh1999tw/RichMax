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
        self.gameService = GameService(
            db) if gameService == None else gameService
        self.userService = UserService(
            db) if userService == None else userService

    def recordAndReply(self, event, view: View):
        self.lineBotApi.reply_message(event.reply_token, view.message)
        self.userService.setLastMessageId(event.source.user_id, view.messageId)


class FollowController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameService=None, userService=None):
        super().__init__(lineBotApi, db, gameService, userService)

    def handleEvent(self, event):
        if isinstance(event, FollowEvent):
            self.recordAndReply(event, ViewFactory.greeting())
        elif isinstance(event, UnfollowEvent):
            self.gameService.leaveGame(event.source.user_id)
            self.userService.delete(event.source.user_id)


class DefaultController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameService=None, userService=None):
        super().__init__(lineBotApi, db, gameService, userService)

    def handleEvent(self, event):
        userId = event.source.user_id
        if isinstance(event, PostbackEvent):
            data = PostbackData.parse(event.postback.data)
            if data.type == PostbackType.CreateGame:
                gameId = self.gameService.createGame(userId)
                self.userService.initGameData(userId)
                self.recordAndReply(event, ViewFactory.gameCreated(ConsoleArgument(
                    gameId,
                    self.lineBotApi.get_profile(
                        userId).display_name,
                    15000)))
            return

        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            if GameService.isGameId(event.message.text):
                if self.gameService.joinGame(event.message.text, userId):
                    self.userService.initGameData(userId)
                    self.recordAndReply(event, ViewFactory.joinGameSuccess(ConsoleArgument(
                        event.message.text,
                        self.lineBotApi.get_profile(
                            userId).display_name,
                        15000)))
                else:
                    self.recordAndReply(event, ViewFactory.joinGameFail())

        self.recordAndReply(event, ViewFactory.greeting())


class GameController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameService=None, userService=None):
        super().__init__(lineBotApi, db, gameService, userService)

    def handleEvent(self, event, gameId: str):
        userId = event.source.user_id
        responseContext = None

        try:
            if isinstance(event, PostbackEvent):
                print(event.postback.data)
                data = PostbackData.parse(event.postback.data)
                if data.type == PostbackType.LeaveConfirm:
                    self.recordAndReply(
                        event, ViewFactory.leaveConfirm(self.getConsoleArgument(gameId, userId)))
                elif data.type == PostbackType.Leave:
                    if self.userService.isLastMessage(userId, data.messageId):
                        self.gameService.leaveGame(userId)
                        self.userService.delete(userId)
                        self.recordAndReply(event, ViewFactory.leavedGame())
                    else:
                        self.recordAndReply(event, ViewFactory.buttonExpired())
                elif data.type == PostbackType.UserInfo:
                    pass
                elif data.type == PostbackType.Earn:
                    responseContext = UserContext(UserContextType.Earn)
                    self.recordAndReply(event, ViewFactory.askEarnAmount())
                elif data.type == PostbackType.Pay:
                    responseContext = UserContext(UserContextType.Pay)
                    self.recordAndReply(event, ViewFactory.askPayAmount())
                elif data.type == PostbackType.Transfer:
                    players = {}
                    for memberId in self.gameService.getMemberIds(gameId, userId):
                        players[memberId] = self.getUserName(memberId)
                    if len(players) <= 0:
                        self.recordAndReply(event, ViewFactory.Console(
                            self.getConsoleArgument(gameId, userId), text="這場遊戲還沒有其他玩家喔~\n快邀請朋友加入吧!"))
                    else:
                        self.recordAndReply(event, ViewFactory.askTransferTarget(
                            self.getConsoleArgument(gameId, userId), players))
                elif data.type == PostbackType.SelectTransferTarget:
                    if self.userService.isLastMessage(userId, data.messageId):
                        responseContext = UserContext(UserContextType.TransferAmount, data.params)
                        self.recordAndReply(event, ViewFactory.askTransferAmount(self.getUserName(data.params)))
                    else:
                        self.recordAndReply(event, ViewFactory.buttonExpired())
                elif data.type == PostbackType.Chance:
                    if data.params == None:
                        cardService = ChanceService(self._db)
                        viewFunc = cardService.draw(gameId)
                        self.recordAndReply(event, viewFunc(self.getConsoleArgument(gameId, userId)))
                elif data.type == PostbackType.Destiny:
                    cardService = DestinyService(self._db)
                    if data.params == None:
                        cardViewFunc = cardService.draw(gameId)
                        self.recordAndReply(event, cardViewFunc(self.getConsoleArgument(gameId, userId)))
                    else:
                        cardService.excuteCard(data.params["name"], event, self, gameId)
                return

            userContext = self.userService.getContext(userId)
            if userContext != None:
                if userContext.type == UserContextType.Earn:
                    try:
                        if not isinstance(event, MessageEvent) or not isinstance(event.message, TextMessage):
                            raise ArgumentError(None, "")
                        amount = int(event.message.text)
                        if amount <= 0:
                            raise ArgumentError(None, "")
                        self.userService.addBalance(userId, amount)
                        self.gameService.AddGameLog(gameId, GameLog(
                            f"{self.getUserName(userId)} 領取了 ${amount}", GameLogAction.Earn, amount))
                        self.recordAndReply(event, ViewFactory.OperateSuccess(
                            self.getConsoleArgument(gameId, userId), f"操作成功~\n您領取了 ${amount}"))
                    except (ArgumentError, ValueError):
                        responseContext = userContext
                        self.recordAndReply(event, ViewFactory.inputError())
                elif userContext.type == UserContextType.Pay:
                    try:
                        if not isinstance(event, MessageEvent) or not isinstance(event.message, TextMessage):
                            raise ArgumentError(None, "")
                        amount = int(event.message.text)
                        if amount <= 0 or amount > self.userService.getBalance(userId):
                            raise ArgumentError(None, "")
                        self.userService.addBalance(userId, amount * -1)
                        self.gameService.AddGameLog(gameId, GameLog(
                            f"{self.getUserName(userId)} 繳納了 ${amount}", GameLogAction.Pay, amount))
                        self.recordAndReply(event, ViewFactory.OperateSuccess(
                            self.getConsoleArgument(gameId, userId), f"操作成功~\n您繳納了 ${amount}"))
                    except (ArgumentError, ValueError):
                        responseContext = userContext
                        self.recordAndReply(event, ViewFactory.inputError())
                elif userContext.type == UserContextType.TransferAmount:
                    try:
                        if not isinstance(event, MessageEvent) or not isinstance(event.message, TextMessage):
                            raise ArgumentError(None, "")
                        amount = int(event.message.text)
                        balance = self.userService.getBalance(userId)
                        if amount <= 0 or amount > balance:
                            raise ArgumentError(None, "")
                        self.userService.addBalance(userContext.params, amount)
                        self.userService.addBalance(userId, amount * -1)
                        toPlayerName = self.getUserName(userContext.params)
                        self.gameService.AddGameLog(gameId, GameLog(
                            f"{self.getUserName(userId)} 匯款給 {toPlayerName} ${amount}",
                            GameLogAction.Transfer,
                            json.dumps(
                                {"from": userId, "to": userContext.params,
                                    "amount": amount},
                                separators=(',', ':')).replace("\"", "\\\"").replace("\n", "")))
                        self.recordAndReply(event, ViewFactory.OperateSuccess(
                            self.getConsoleArgument(gameId, userId), f"操作成功~\n您匯了 ${amount} 給 {toPlayerName}"))
                    except (ArgumentError, ValueError) as ex:
                        responseContext = userContext
                        self.recordAndReply(event, ViewFactory.inputError())
                return

            self.recordAndReply(
                event, ViewFactory.Console(self.getConsoleArgument(gameId, userId)))
        finally:
            self.userService.setContext(userId, responseContext)

    def getConsoleArgument(self, gameId: str, userId: str):
        return ConsoleArgument(
            gameId,
            self.lineBotApi.get_profile(userId).display_name,
            self.userService.getBalance(userId),
            self.gameService.getGameLogs(gameId))

    def getUserName(self, userId):
        return self.lineBotApi.get_profile(userId).display_name
