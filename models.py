from datetime import datetime
import json
import uuid


class PostbackData:
    def __init__(self, action:str, messageId="", params=None):
        self.action = action
        self.messageId = messageId
        self.params = params

    def toFormatedJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, separators=(',', ':')).replace("\"", "\\\"").replace("\n","")

    def parse(value: str):
        data = json.loads(value.replace("\\\"", "\""))
        return PostbackData(data["action"], data["messageId"], data["params"])

class PostbackAction:
    CreateGame = "CreateGame"
    LeaveConfirm = "LeaveConfirm"
    Leave = "Leave"
    UserInfo = "UserInfo"
    Earn = "Earn"
    Pay = "Pay"
    Transfer = "Transfer"
    Chance = "Chance"
    Destiny = "Destiny"

class GameLog:
    def __init__(self, message: str, action: str, value, id = None, time = None, canceled = False):
        self.id = str(uuid.uuid4()) if id == None else id
        self.time = datetime.now() if time == None else time
        self.message = message
        self.action = action
        self.value = value
        self.canceled = canceled
    
    def parse(obj: dict):
        return GameLog(obj["message"], obj["action"], obj["value"], obj["id"], obj["time"], obj["canceled"])

    def toDict(self):
        return {
            "id": self.id,
            "time": self.time,
            "message": self.message,
            "action": self.action,
            "value": self.value,
            "canceled": self.canceled
        }

    def __str__(self):
        return f"{self.message}{'(已取消)' if self.canceled else ''}"

class GameLogAction:
    Earn = "Earn"
    Pay = "Pay"
    Transfer = "Transfer"
