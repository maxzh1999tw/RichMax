from datetime import datetime
import json
import uuid

class PostbackData:
    def __init__(self, type:str, messageId="", params=None):
        self.type = type
        self.messageId = messageId
        self.params = params

    def toFormatedJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, separators=(',', ':')).replace("\"", "\\\"").replace("\n","")

    def parse(value: str):
        data = json.loads(value.replace("\\\"", "\""))
        return PostbackData(data["type"], data["messageId"], data["params"])

class PostbackType:
    Console = "Console"
    Rollback = "Rollback"
    CreateGame = "CreateGame"
    LeaveConfirm = "LeaveConfirm"
    Leave = "Leave"
    UserInfo = "UserInfo"
    Earn = "Earn"
    Pay = "Pay"
    Transfer = "Transfer"
    SelectTransferTarget = "SelectTransferTarget"
    Chance = "Chance"
    Destiny = "Destiny"

class GameLog:
    def __init__(self, name: str, message: str, action: str, value, id = None, time = None, canceled = False):
        self.name = name
        self.id = str(uuid.uuid4()) if id == None else id
        self.time = datetime.now() if time == None else time
        self.message = message
        self.action = action
        self.value = value
        self.canceled = canceled
    
    def parse(obj: dict):
        return GameLog(obj["name"], obj["message"], obj["action"], obj["value"], obj["id"], obj["time"], obj["canceled"])

    def __iter__(self):
        for key in self.__dict__:
            yield key, getattr(self, key)

    def __str__(self):
        return f"{self.message}{' (已撤銷)' if self.canceled else ''}"

class GameLogAction:
    Earn = "Earn"
    Pay = "Pay"
    Transfer = "Transfer"

class UserContext:
    def __init__(self, type: str, params=None):
        self.type = type
        self.params = params

    def __iter__(self):
        for key in self.__dict__:
            yield key, getattr(self, key)
    
    def parse(obj: dict):
        return UserContext(obj["type"], obj["params"]) if obj != None else None


class UserContextType:
    Earn = "Earn"
    Pay = "Pay"
    TransferAmount = "TransferAmount"