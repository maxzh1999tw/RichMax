import json


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