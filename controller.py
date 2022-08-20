from argparse import ArgumentError
from linebot import LineBotApi
from linebot.models import *
from google.cloud.firestore import Client
from postback import PostbackData, PostbackAction

from services import GameService, UserService
from view import ConsoleArgument, View, ViewFactory


class BaseController:
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameService=None, userService=None):
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
            if data.action == PostbackAction.CreateGame:
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
                    self.userService.initGameData()
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
                data = PostbackData.parse(event.postback.data)
                if data.action == PostbackAction.LeaveConfirm:
                    self.recordAndReply(
                        event, ViewFactory.leaveConfirm(self.getConsoleArgument(gameId, userId)))
                elif data.action == PostbackAction.Leave:
                    if self.userService.isLastMessage(userId, data.messageId):
                        self.gameService.leaveGame(userId)
                        self.userService.delete(userId)
                        self.recordAndReply(event, ViewFactory.leavedGame())
                    else:
                        self.recordAndReply(event, ViewFactory.buttonExpired())
                elif data.action == PostbackAction.UserInfo:
                    pass
                elif data.action == PostbackAction.Earn:
                    responseContext = "Earn"
                    self.recordAndReply(event, ViewFactory.askEarnAmount())
                elif data.action == PostbackAction.Pay:
                    responseContext = "Pay"
                    self.recordAndReply(event, ViewFactory.askPayAmount())
                return

            userContext = self.userService.getContext(userId)
            if userContext != None:
                if userContext == "Earn":
                    try:
                        if not isinstance(event, MessageEvent) or not isinstance(event.message, TextMessage):
                            raise ArgumentError()
                        amount = int(event.message.text)
                        if amount <= 0:
                            raise ArgumentError()
                        self.userService.addBalance(userId, amount)
                        self.recordAndReply(event, ViewFactory.OperateSuccess(
                            self.getConsoleArgument(gameId, userId), f"操作成功~\n您領取了 ${amount}"))
                        self.gameService.logGameRecord(
                            gameId, f"{self.getUserName(userId)} 領取了 ${amount}")
                    except ArgumentError:
                        responseContext = userContext
                        self.recordAndReply(event, ViewFactory.inputError())
                elif userContext == "Pay":
                    try:
                        if not isinstance(event, MessageEvent) or not isinstance(event.message, TextMessage):
                            raise ArgumentError()
                        amount = int(event.message.text)
                        if amount <= 0:
                            raise ArgumentError()
                        self.userService.addBalance(userId, amount * -1)
                        self.recordAndReply(event, ViewFactory.OperateSuccess(
                            self.getConsoleArgument(gameId, userId), f"操作成功~\n您繳納了 ${amount}"))
                        self.gameService.logGameRecord(
                            gameId, f"{self.getUserName(userId)} 繳納了 ${amount}")
                    except ArgumentError:
                        responseContext = userContext
                        self.recordAndReply(event, ViewFactory.inputError())
                return

            self.recordAndReply(
                event, ViewFactory.Console(self.getConsoleArgument(gameId, userId)))
        finally:
            self.userService.setContext(userId, responseContext)

    def getConsoleArgument(self, gameId: str, userId: str):
        return ConsoleArgument(gameId, self.lineBotApi.get_profile(
            userId).display_name, self.userService.getBalance(userId))

    def getUserName(self, userId):
        return self.lineBotApi.get_profile(userId).display_name
