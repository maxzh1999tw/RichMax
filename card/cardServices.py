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

    def excuteCard(self, controller):
        self.cardDict[controller.data.params["name"]][0](
            controller.userId, controller, controller.gameId, controller.data.params)

    def balanceCardExcution(self, userId, controller, gameId: str, action: str, amount: int, reason: str):
        controller.userService.addBalance(userId, amount if action == GameLogAction.Earn else amount * -1)
        text = f"{reason}，" + ("得到" if action == GameLogAction.Earn else "失去") + f"了 ${amount}"
        gameLog = GameLog(controller.getUserName(userId), text, GameLogAction.Earn, amount)
        controller.gameService.AddGameLog(gameId, gameLog)
        text = "領取" if action == GameLogAction.Earn else "繳納"
        controller.recordAndReply(ViewFactory.OperateSuccess(
            controller.getConsoleArgument(), f"操作成功~\n您{text}了 ${amount}", gameLog.id))

class DestinyService(BaseCardService):
    def __init__(self, db: Client):
        cardDict = {
            "外星人俘虜": (None, lambda argument : CardViewFactory.capturedByAliens(argument)),
            "牢底坐穿": (None, lambda argument : CardViewFactory.goToJail(argument)),
            "家人的呼喚": (self.backHome, lambda argument : CardViewFactory.backHome(argument)),
            "土地我做主": (None, lambda argument : CardViewFactory.buildMyLand(argument)),
            "生日快樂": (None, lambda argument : CardViewFactory.happyBirthday(argument)),
            "擊落戰鬥機": (self.shootDownFighter, lambda argument : CardViewFactory.shootDownFighter(argument)),
            "繳學費": (self.payTuition, lambda argument : CardViewFactory.payTuition(argument)),
            "超速罰單": (self.speedingTicket, lambda argument : CardViewFactory.speedingTicket(argument)),
            "小本生意": (self.smallBusiness, lambda argument : CardViewFactory.smallBusiness(argument)),
            "中頭彩": (self.jackpot, lambda argument : CardViewFactory.jackpot(argument)),
            "All in 比特幣":(self.allInBitcoin, lambda argument : CardViewFactory.allInBitcoin(argument)),
            "詐騙集團": (self.scammed, lambda argument : CardViewFactory.scammed(argument))
        }
        super().__init__(db, "DestinyCards", cardDict)

    def shootDownFighter(self, userId, controller, gameId: str, params):
        self.balanceCardExcution(userId, controller, gameId, GameLogAction.Earn, 3000, "擊落戰鬥機")

    def payTuition(self, userId, controller, gameId: str, params):
        self.balanceCardExcution(userId, controller, gameId, GameLogAction.Pay, 600, "繳學費")

    def backHome(self, userId, controller, gameId: str, params):
        self.balanceCardExcution(userId, controller, gameId, GameLogAction.Earn, 2000, "回到起點")

    def speedingTicket(self, userId, controller, gameId: str, params):
        self.balanceCardExcution(userId, controller, gameId, GameLogAction.Pay, params["amount"], "超速被拍")

    def smallBusiness(self, userId, controller, gameId: str, params):
        self.balanceCardExcution(userId, controller, gameId, GameLogAction.Earn, 1000, "經營小本生意")

    def jackpot(self, userId, controller, gameId: str, params):
        self.balanceCardExcution(userId, controller, gameId, GameLogAction.Earn, 2000, "中頭彩")

    def allInBitcoin(self, userId, controller, gameId: str, params):
        balance = controller.userService.getBalance(userId)
        amount = balance if params["earn"] else balance // 2
        action = GameLogAction.Earn if params["earn"] else GameLogAction.Pay
        text = "All in 比特幣" + ("大賺" if params["earn"] else "慘賠")
        self.balanceCardExcution(userId, controller, gameId, action, amount, text)

    def scammed(self, userId, controller, gameId: str, params):
        self.balanceCardExcution(userId, controller, gameId, GameLogAction.Pay, 1200, "詐騙集團")


class ChanceService(BaseCardService):
    def __init__(self, db: Client):
        cardDict = {
            "股票當沖": (self.stockHit, lambda argument : CardViewFactory.stockHit(argument, 3)),
            "豪華坐駕": (None, lambda argument : CardViewFactory.tripleDice(argument)),
            "都更協調會": (None, lambda argument : CardViewFactory.urbanRenewal(argument)),
            "有關係沒關係": (None, lambda argument : CardViewFactory.notGuilty(argument)),
            "公共運輸": (None, lambda argument : CardViewFactory.goToStation(argument)),
            "進退有據": (None, lambda argument : CardViewFactory.forwardOrBackward(argument)),
            "儲蓄險": (None, lambda argument : CardViewFactory.wholeLife(argument)),
            "超額保險": (None, lambda argument : CardViewFactory.excessInsurance(argument)),
            "一起走": (None, lambda argument : CardViewFactory.takeMeAway(argument)),
            "沒關係有關係": (None, lambda argument : CardViewFactory.youGoToJail(argument)),
            "施比受更有福": (None, lambda argument : CardViewFactory.giveLand(argument)),
            "莫拉克風災": (None, lambda argument : CardViewFactory.fixHouse(argument)),
            "天手力": (None, lambda argument : CardViewFactory.changePosition(argument)),
            "不給機會": (None, lambda argument : CardViewFactory.antiChance(argument)), 
        }
        super().__init__(db, "ChanceCards", cardDict)

    def stockHit(self, userId, controller, gameId: str, params):
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
        controller.gameService.AddGameLog(gameId, GameLog(controller.getUserName(userId),
            f"玩股票當沖，{text}了 ${amount}", resultType, amount))

        argument = controller.getConsoleArgument()
        text = f"當沖失敗...您失去了 ${amount}" if resultType == GameLogAction.Pay else f"當沖賺錢!!您獲得了 ${amount}"
        if params["times"] == 1:
            controller.recordAndReply(ViewFactory.Console(argument, text=text))
        else:
            controller.recordAndReply(CardViewFactory.stockHit(argument, params["times"] - 1, text))