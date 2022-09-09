from datetime import datetime, timedelta
from heapq import merge
import random
from google.cloud import firestore
from google.cloud.firestore import Client

from models import GameLog, UserContext


class GameService:

    def __init__(self, db: Client):
        self._db = db
        self._collection = self._db.collection("Game")

    def getUserGameId(self, userId: str):
        docs = self._collection.where(
            "Members", "array_contains", userId).get()
        for doc in docs:
            if datetime.now() - doc.get("UpdateTime").replace(tzinfo=None) > timedelta(hours=10):
                doc.reference.delete()
                return None
            return doc.id
        return None

    def createGame(self, *memberIds: str):
        while True:
            gameId = f"{random.randint(0, 9999):04}"
            gameDoc = self._collection.document(gameId)
            if not gameDoc.get().exists:
                break
        gameDoc.create({
            "UpdateTime": datetime.now(),
            "Members": memberIds,
            "GameLogs": [],
            "DestinyCards": [],
            "ChanceCards":[]
        })
        return gameId

    def isGameId(value: str):
        if len(value) == 4:
            for char in value:
                if not char.isnumeric():
                    return False
            return True
        return False

    def joinGame(self, gameId: str, userId: str):
        doc_snap = self._collection.document(gameId)
        doc = doc_snap.get()
        if not doc.exists:
            return False

        doc_snap.update({
            "Members": firestore.ArrayUnion([userId])
        })
        return True

    def leaveGame(self, userId: str):
        docs = self._collection.where(
            "Members", "array_contains", userId).get()
        for doc in docs:
            if len(doc.get("Members")) == 1:
                doc.reference.delete()
            else:
                doc.reference.update({
                    "Members": firestore.ArrayRemove([userId])
                })

    def AddGameLog(self, gameId: str, gameLog: GameLog):
        self._collection.document(gameId).update({
            "GameLogs": firestore.ArrayUnion([dict(gameLog)])
        })

    def getGameLogs(self, gameId: str):
        logs = self._collection.document(gameId).get().get("GameLogs")[-7:]
        result = []
        for log in logs:
            result.append(GameLog.parse(log))
        return result

    def getGameLog(self, gameId: str, gameLogId: str) -> GameLog:
        logs = self._collection.document(gameId).get().get("GameLogs")
        return GameLog.parse([x for x in logs if x["id"] == gameLogId][0])

    def rollbackGameLog(self, gameId: str, gameLogId: str):
        logs = self._collection.document(gameId).get().get("GameLogs")
        for log in logs:
            if log["id"] == gameLogId:
                log["canceled"] = True
        self._collection.document(gameId).update({
            "GameLogs": logs
        })

    def getOtherMembers(self, gameId: str, excludeId: str):
        memberIds = self._collection.document(gameId).get().get("Members")
        memberIds.remove(excludeId)
        return memberIds


class UserService:
    initBalance = 15000

    def __init__(self, db: Client):
        self._db = db
        self._collection = self._db.collection("User")

    def setLastMessageId(self, userId: str, messageId: str):
        self._collection.document(userId).set({
            "LastMessageId": messageId
        }, merge=True)

    def isLastMessage(self, userId: str, messageId: str):
        doc = self._collection.document(userId)
        if not doc.get().exists:
            return False
        return messageId == doc.get().get("LastMessageId")

    def delete(self, userId):
        doc = self._collection.document(userId)
        if doc.get().exists:
            doc.delete()

    def initGameData(self, userId: str):
        self._collection.document(userId).set({
            "Balance": UserService.initBalance,
            "Context": None,
        }, merge=True)

    def getBalance(self, userId):
        return self._collection.document(userId).get().get("Balance")

    def getContext(self, userId: str):
        return UserContext.parse(self._collection.document(userId).get().get("Context"))

    def setContext(self, userId: str, context: UserContext):
        doc = self._collection.document(userId)
        if doc.get().exists:
            self._collection.document(userId).update({
                "Context": dict(context) if context != None else None
            })

    def addBalance(self, userId: str, amount: int):
        doc = self._collection.document(userId)
        if doc.get().exists:
            doc.update({
                "Balance": firestore.Increment(amount)
            })
