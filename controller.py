from linebot import LineBotApi
from linebot.models import *
from google.cloud.firestore import Client
from postback import PostbackData, PostbackAction

from services import GameService, UserService
from view import ConsoleArgument, View, ViewFactory


class BaseController:
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameService=None, userService=None):
        self.lineBotApi = lineBotApi
        self.gameService = GameService(db) if gameService == None else gameService
        self.userService = UserService(db) if userService == None else userService

    def recordAndReply(self, event, view: View):
        self.userService.setLastMessageId(event.source.user_id, view.messageId)
        self.lineBotApi.reply_message(event.reply_token, view.message)


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
        if isinstance(event, PostbackEvent):
            data = PostbackData.parse(event.postback.data)
            if data.action == PostbackAction.CreateGame:
                gameId = self.gameService.createGame(event.source.user_id)
                self.recordAndReply(event, ViewFactory.gameCreated(ConsoleArgument(
                    gameId,
                    self.lineBotApi.get_profile(
                        event.source.user_id).display_name,
                    GameService.initBalace)))
            return

        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            if GameService.isGameId(event.message.text):
                if self.gameService.joinGame(event.message.text, event.source.user_id):
                    self.recordAndReply(event, ViewFactory.joinGameSuccess(ConsoleArgument(
                        event.message.text,
                        self.lineBotApi.get_profile(
                            event.source.user_id).display_name,
                        GameService.initBalace)))
                else:
                    self.recordAndReply(event, ViewFactory.joinGameFail())

        self.recordAndReply(event, ViewFactory.greeting())


class GameController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client, gameService=None, userService=None):
        super().__init__(lineBotApi, db, gameService, userService)

    def handleEvent(self, event, gameId:str):
        self.consoleArgument = ConsoleArgument(gameId, self.lineBotApi.get_profile(
            event.source.user_id).display_name, 15000)
        if isinstance(event, PostbackEvent):
            data = PostbackData.parse(event.postback.data)
            if data.action == PostbackAction.LeaveConfirm:
                self.recordAndReply(
                    event, ViewFactory.leaveConfirm(self.consoleArgument))
            elif data.action == PostbackAction.Leave:
                if self.userService.isLastMessage(event.source.user_id, data.messageId):
                    self.gameService.leaveGame(event.source.user_id)
                    self.recordAndReply(event, ViewFactory.leavedGame())
            elif data.action == PostbackAction.UserInfo:
                pass
            return

        self.recordAndReply(
            event, ViewFactory.textWithConsole(self.consoleArgument))
