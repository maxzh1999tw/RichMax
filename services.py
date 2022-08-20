from datetime import datetime, timedelta
import random
from google.cloud import firestore
from google.cloud.firestore import Client


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
            "Records": [],
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

    def logGameRecord(self, gameId: str, record: str):
        self._collection.document(gameId).update({
            "Records": firestore.ArrayUnion(record)
        })


class UserService:
    _initBalance = 15000

    def __init__(self, db: Client):
        self._db = db
        self._collection = self._db.collection("User")

    def setLastMessageId(self, userId: str, messageId: str):
        self._collection.document(userId).update({
            "LastMessageId": messageId
        })

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
        self._collection.document(userId).update({
            "Balance": UserService._initBalance,
            "Context": None,
        })

    def getBalance(self, userId):
        return self._collection.document(userId).get().get("Balance")

    def getContext(self, userId: str):
        return self._collection.document(userId).get().get("Context")

    def setContext(self, userId: str, context):
        self._collection.document(userId).update({
            "Context": context
        })

    def addBalance(self, userId: str, amount: int):
        self._collection.document(userId).update({
            "Balance": firestore.Increment(amount)
        })
