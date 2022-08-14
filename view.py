import json
import uuid
from linebot.models import *

from postback import PostbackData, PostbackAction


class View:
    def __init__(self, messageId: str, message):
        self.messageId = messageId
        self.message = message


class ConsoleArgument:
    def __init__(self, gameId: str, username: str, balance: int):
        self.gameId = gameId
        self.username = username
        self.balance = balance


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
            "@CreateGame", PostbackData(PostbackAction.CreateGame).toFormatedJSON())
        return View("", FlexSendMessage(alt_text="請建立或加入遊戲", contents=json.loads(template, strict=False)))

    def joinGameFail():
        return View("", TextSendMessage(text="加入失敗，請輸入正確的房號"))

    def leavedGame():
        return View("", TextSendMessage(text="您已經退出遊戲"))

    def gameCreated(argument: ConsoleArgument):
        return ViewFactory.textWithConsole(argument, text=f"您建立了新遊戲\n房號為: {argument.gameId}\n快邀請朋友加入吧~")

    def joinGameSuccess(argument: ConsoleArgument):
        return ViewFactory.textWithConsole(argument, text=f"您加入了遊戲\n快邀請朋友加入吧~")

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
            "@Leave", PostbackData(PostbackAction.Leave, id).toFormatedJSON())
        message = json.loads(template, strict=False)
        message["header"] = ViewFactory._getGameHeader(argument)
        return View(id, FlexSendMessage(alt_text="您確定要退出嗎?", contents=message))

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

    def textWithConsole(argument: ConsoleArgument, *bubbles: BubbleContainer, text=None):
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
        id = str(uuid.uuid4())
        template = template.replace(
            "@Earn", PostbackData("Earn", id).toFormatedJSON())
        template = template.replace(
            "@Pay", PostbackData("Pay", id).toFormatedJSON())
        template = template.replace(
            "@Transfer", PostbackData("Transfer", id).toFormatedJSON())
        template = template.replace(
            "@Chance", PostbackData("Chance", id).toFormatedJSON())
        template = template.replace(
            "@Destiny", PostbackData("Destiny", id).toFormatedJSON())
        template = template.replace(
            "@LeaveConfirm", PostbackData(PostbackAction.LeaveConfirm, id).toFormatedJSON())
        template = template.replace(
            "@UserInfo", PostbackData(PostbackAction.UserInfo, id).toFormatedJSON())
        message = json.loads(template, strict=False)
        message["contents"][0]["header"] = ViewFactory._getGameHeader(argument)
        for bubble in bubbles:
            message["contents"].append(bubble)
        alt_text = text
        if text != None:
            template = message["contents"][0]["body"]["contents"][0]["text"] = text
        else:
            del message["contents"][0]["body"]
            alt_text = "控制面板"
        return View(id, FlexSendMessage(alt_text=alt_text, contents=message))
