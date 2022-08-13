from datetime import datetime, timedelta
import random
from google.cloud import firestore
from google.cloud.firestore import Client


class GameService:
    initBalace = 150000

    def __init__(self, db: Client):
        self.db = db
        self.collection = self.db.collection("Game")

    def getUserGameId(self, userId: str):
        docs = self.collection.where("Members", "array_contains", userId).get()
        for doc in docs:
            if datetime.now() - doc.get("UpdateTime").replace(tzinfo=None) > timedelta(hours=10):
                doc.reference.delete()
                return None
            return doc.id
        return None

    def createGame(self, *memberIds: str):
        while True:
            gameId = f"{random.randint(0, 9999):04}"
            gameDoc = self.collection.document(gameId)
            if not gameDoc.get().exists:
                break
        gameDoc.create({
            "UpdateTime": datetime.now(),
            "Members": memberIds,
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
        doc_snap = self.collection.document(gameId)
        doc = doc_snap.get()
        if not doc.exists:
            return False

        doc_snap.update({
            "Members": firestore.ArrayUnion([userId])
        })
        return True

    def leaveGame(self, userId: str):
        docs = self.collection.where("Members", "array_contains", userId).get()
        for doc in docs:
            if len(doc.get("Members")) == 1:
                doc.reference.delete()
            else:
                doc.reference.update({
                    "Members": firestore.ArrayRemove([userId])
                })


class UserService:
    def __init__(self, db: Client):
        self.db = db
        self.collection = self.db.collection("User")

    def setLastMessageId(self, userId: str, messageId: str):
        doc = self.collection.document(userId)
        if not doc.get().exists:
            doc.create({
                "LastMessageId": messageId
            })
        else:
            doc.update({
                "LastMessageId": messageId
            })

    def isLastMessage(self, userId: str, messageId: str):
        doc = self.collection.document(userId)
        if not doc.get().exists:
            return False
        return messageId == doc.get().get("LastMessageId")

    def delete(self, userId):
        doc = self.collection.document(userId)
        if doc.get().exists:
            doc.delete()
