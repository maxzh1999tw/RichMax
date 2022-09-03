from datetime import datetime
import json
import uuid
from linebot.models import *

from models import GameLog, PostbackData, PostbackType


class View:
    def __init__(self, messageId: str, message):
        self.messageId = messageId
        self.message = message


class ConsoleArgument:
    def __init__(self, gameId: str, username: str, balance: int, logs: list = []):
        self.gameId = gameId
        self.username = username
        self.balance = balance
        self.logs = logs


class ViewFactory:
    def greeting():
        template = """
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "您還沒有加入遊戲，\n請直接輸入房號來加入，\n或點擊下方按鈕建立新遊戲。",
                            "wrap": true
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "建立新遊戲",
                                "data": "@CreateGame"
                            }
                        }
                    ]
                }
            }
        """
        template = template.replace(
            "@CreateGame", PostbackData(PostbackType.CreateGame).toFormatedJSON())
        return View("", FlexSendMessage(alt_text="請建立或加入遊戲", contents=json.loads(template, strict=False)))

    def joinGameFail():
        return View("", TextSendMessage(text="加入失敗，請輸入正確的房號"))

    def leavedGame():
        return View("", TextSendMessage(text="您已經退出遊戲"))

    def gameCreated(argument: ConsoleArgument):
        return ViewFactory.Console(argument, text=f"您建立了新遊戲\n房號為: {argument.gameId}\n快邀請朋友加入吧~")

    def joinGameSuccess(argument: ConsoleArgument):
        return ViewFactory.Console(argument, text=f"您加入了遊戲\n快邀請朋友加入吧~")

    def leaveConfirm(argument: ConsoleArgument):
        template = """{
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "退出遊戲後所有資產都會被清算\n您確定要退出嗎?",
                        "wrap": true
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "確定",
                            "data": "@Leave"
                        }
                    }
                ]
            }
        }"""
        id = str(uuid.uuid4())
        template = template.replace(
            "@Leave", PostbackData(PostbackType.Leave, id).toFormatedJSON())
        message = json.loads(template, strict=False)
        message["header"] = ViewFactory._getGameHeader(argument)
        return View(id, FlexSendMessage(alt_text="您確定要退出嗎?", contents=message))

    def buttonExpired():
        return TextSendMessage(text="阿噢，這顆按鈕已經過期了，請重新呼叫選單~")

    def askEarnAmount():
        return View("",  TextSendMessage(
            text="您要領取多少錢",
            quick_reply=QuickReply([
                QuickReplyButton(action=MessageAction(
                    label="2000", text="2000")),
            ])))

    def askPayAmount():
        return View("", TextSendMessage(
            text="您要繳多少錢",
            quick_reply=QuickReply([
                QuickReplyButton(action=MessageAction(
                    label="2000", text="2000")),
            ])))

    def askTransferTarget(argument: ConsoleArgument, players: dict):
        template = """{
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "請選擇匯款對象",
                        "wrap": true
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                
                ]
            }
        }"""
        id = str(uuid.uuid4())
        message = json.loads(template, strict=False)
        message["header"] = ViewFactory._getGameHeader(argument)
        for playerId, playerName in players.items():
            message["footer"]["contents"].append(ButtonComponent(action=PostbackAction(
                label=playerName, data=PostbackData(PostbackType.SelectTransferTarget, id, playerId).toFormatedJSON())))
        return View(id, FlexSendMessage(alt_text="請選擇匯款對象", contents=message))

    def askTransferAmount(toPlayerName: str):
        return View("", TextSendMessage(text=f"您要匯給 {toPlayerName} 多少錢"))

    def inputError():
        return View("", TextSendMessage(text="輸入錯誤，請重新輸入"))

    def OperateSuccess(argument: ConsoleArgument, text: str):
        return ViewFactory.Console(argument, text=text)

    def _getGameHeader(argument: ConsoleArgument):
        template = """{
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "[@gameId] @username"
                },
                {
                    "type": "text",
                    "text": "餘額: @balance"
                }
            ],
            "alignItems": "center"
        }"""
        template = template.replace("@gameId", argument.gameId)
        template = template.replace("@username", argument.username)
        template = template.replace(
            "@balance", "{:,}".format(argument.balance))
        return json.loads(template, strict=False)

    def Console(argument: ConsoleArgument, *bubbles: BubbleContainer, text=None, id=""):
        template = """{
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "@text",
                                "wrap": true
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "postback",
                                            "label": "領錢",
                                            "data": "@Earn"
                                        },
                                        "style": "primary"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "postback",
                                            "label": "繳錢",
                                            "data": "@Pay"
                                        },
                                        "style": "primary"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "postback",
                                            "label": "匯錢",
                                            "data": "@Transfer"
                                        },
                                        "style": "primary"
                                    }
                                ],
                                "spacing": "md"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "postback",
                                            "label": "機會",
                                            "data": "@Chance"
                                        },
                                        "style": "secondary"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "postback",
                                            "label": "命運",
                                            "data": "@Destiny"
                                        },
                                        "style": "secondary"
                                    }
                                ],
                                "spacing": "md"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "image",
                                        "url": "https://cdn-icons-png.flaticon.com/512/1946/1946429.png",
                                        "size": "25px",
                                        "align": "start",
                                        "action": {
                                            "type": "postback",
                                            "label": "action",
                                            "data": "@UserInfo"
                                        }
                                    },
                                    {
                                        "type": "image",
                                        "url": "https://cdn-icons-png.flaticon.com/512/402/402718.png",
                                        "size": "25px",
                                        "align": "end",
                                        "action": {
                                            "type": "postback",
                                            "label": "action",
                                            "data": "@LeaveConfirm"
                                        }
                                    }
                                ],
                                "alignItems": "flex-end",
                                "margin": "xl",
                                "paddingStart": "md",
                                "paddingEnd": "md",
                                "paddingBottom": "xs"
                            }
                        ],
                        "spacing": "md"
                    }
                }
            ]
        }"""
        template = template.replace(
            "@Earn", PostbackData(PostbackType.Earn, id).toFormatedJSON())
        template = template.replace(
            "@Pay", PostbackData(PostbackType.Pay, id).toFormatedJSON())
        template = template.replace(
            "@Transfer", PostbackData(PostbackType.Transfer, id).toFormatedJSON())
        template = template.replace(
            "@Chance", PostbackData(PostbackType.Chance, id).toFormatedJSON())
        template = template.replace(
            "@Destiny", PostbackData(PostbackType.Destiny, id).toFormatedJSON())
        template = template.replace(
            "@LeaveConfirm", PostbackData(PostbackType.LeaveConfirm, id).toFormatedJSON())
        template = template.replace(
            "@UserInfo", PostbackData(PostbackType.UserInfo, id).toFormatedJSON())
        message = json.loads(template, strict=False)
        message["contents"][0]["header"] = ViewFactory._getGameHeader(argument)
        if len(argument.logs) > 0:
            message["contents"].append(
                ViewFactory._getGameLogBubble(argument.logs))
        for bubble in bubbles:
            message["contents"].append(bubble)
        alt_text = text
        if text != None:
            template = message["contents"][0]["body"]["contents"][0]["text"] = text
        else:
            message["contents"][0]["body"]["contents"] = []
            alt_text = "控制面板"
        return View(id, FlexSendMessage(alt_text=alt_text, contents=message))

    def _getGameLogBubble(logs: list[GameLog]):
        template = """{
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "操作紀錄",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [
                            
                        ]
                    }
                ]
            },
            "styles": {
                "footer": {
                    "separator": true
                }
            }
        }"""
        message = json.loads(template, strict=False)
        for log in logs:
            time = (datetime.now() - log.time.replace(tzinfo=None)).seconds
            if time < 3:
                text = "剛剛"
            elif time < 60:
                text = f"{time}秒前"
            else:
                time //= 60
                text = f"{time}分鐘前" if time < 60 else f"{time//60}小時前"

            message["body"]["contents"][2]["contents"].append(
                BoxComponent(layout="horizontal", contents=[
                    TextComponent(text=str(log), size="sm",
                                  color="#555555", flex=3,wrap=True),
                    TextComponent(
                        text=text,
                        size="sm", color="#555555", flex=0, align_items="end", margin="md"),
                ]))

        return message
