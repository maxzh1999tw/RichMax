from ast import Lambda
import random
from google.cloud import firestore
from google.cloud.firestore import Client
from card.cardViews import CardViewFactory

from models import GameLog, GameLogAction
from views import ViewFactory


class BaseCardService:
    def __init__(self, db: Client, fieldName: str, cardDict: dict):
        self._db = db
        self._collection = self._db.collection("Game")
        self.fieldName = fieldName
        self.cardDict = cardDict

    def draw(self, gameId: str) -> Lambda:
        isNewDeck = False
        doc = self._collection.document(gameId)
        deck = doc.get().get(self.fieldName)
        if len(deck) == 0:
            deck = self.createNewDeck()
            isNewDeck = True
        card = random.choice(deck)
        if isNewDeck:
            deck.remove(card)
            doc.update({
                self.fieldName: deck
            })
        else:
            doc.update({
                self.fieldName: firestore.ArrayRemove([card])
            })
        return self.cardDict[card][1]

    def createNewDeck(self) -> list:
        return list(self.cardDict.keys())

    def excuteCard(self, card, event, controller, gameId, params=None):
        self.cardDict[card][0](event, controller, gameId, params)


class DestinyService(BaseCardService):
    def __init__(self, db: Client):
        cardDict = {
            "擊落戰鬥機": (self.shootDownFighter, lambda argument : CardViewFactory.shootDownFighter(argument)),
            "繳學費": (self.payTuition, lambda argument : CardViewFactory.payTuition(argument)),
            "外星人俘虜": (None, lambda argument : CardViewFactory.capturedByAliens(argument)),
            "牢底坐穿": (None, lambda argument : CardViewFactory.goToJail(argument)),
        }
        super().__init__(db, "DestinyCards", cardDict)

    def shootDownFighter(self, event, controller, gameId: str, params):
        userId = event.source.user_id
        amount = 2000
        controller.userService.addBalance(userId, amount)
        controller.gameService.AddGameLog(gameId, GameLog(
            f"{controller.getUserName(userId)} 擊落戰鬥機，得到了 ${amount}", GameLogAction.Earn, amount))
        controller.recordAndReply(event, ViewFactory.OperateSuccess(
            controller.getConsoleArgument(gameId, userId), f"操作成功~\n您領取了 ${amount}"))

    def payTuition(self, event, controller, gameId: str, params):
        userId = event.source.user_id
        amount = 600
        controller.userService.addBalance(userId, amount * -1)
        controller.gameService.AddGameLog(gameId, GameLog(
            f"{controller.getUserName(userId)} 繳學費，失去了 ${amount}", GameLogAction.Pay, amount))
        controller.recordAndReply(event, ViewFactory.OperateSuccess(
            controller.getConsoleArgument(gameId, userId), f"操作成功~\n您繳納了 ${amount}"))


class ChanceService(BaseCardService):
    def __init__(self, db: Client):
        cardDict = {
            "股票當沖": (self.stockHit, lambda argument : CardViewFactory.stockHit(argument, 3)),
            "豪華坐駕": (None, lambda argument : CardViewFactory.tripleDice(argument)),
            "都更協調會": (None, lambda argument : CardViewFactory.urbanRenewal(argument)),
            "有關係沒關係": (None, lambda argument : CardViewFactory.notGuilty(argument)),
        }
        super().__init__(db, "ChanceCards", cardDict)

    def stockHit(self, event, controller, gameId: str, params):
        userId = event.source.user_id
        resultType = GameLogAction.Pay
        if params["dice"] == 1:
            resultType = GameLogAction.Earn
            amount = 1000
        elif params["dice"] == 2:
            amount = 200
        elif params["dice"] == 3:
            amount = 300
        elif params["dice"] == 4:
            resultType = GameLogAction.Earn
            amount = 400
        elif params["dice"] == 5:
            amount = 500
        elif params["dice"] == 6:
            amount = 600

        controller.userService.addBalance(
            userId, amount if resultType == GameLogAction.Earn else amount * -1)
        text = "獲得" if resultType == GameLogAction.Earn else "失去"
        controller.gameService.AddGameLog(gameId, GameLog(
            f"{controller.getUserName(userId)} 玩股票當沖，{text}了 ${amount}", resultType, amount))

        argument = controller.getConsoleArgument(gameId, userId)
        text = f"當沖失敗...您失去了 ${amount}" if resultType == GameLogAction.Pay else f"當沖賺錢!!您獲得了 ${amount}"
        if params["times"] == 1:
            controller.recordAndReply(event, ViewFactory.Console(argument, text=text))
        else:
            controller.recordAndReply(event, CardViewFactory.stockHit(argument, params["times"] - 1, text))