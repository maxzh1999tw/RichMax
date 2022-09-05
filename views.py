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
        template = """{
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "wrap": true,
                    "contents": [
                    {
                        "type": "span",
                        "text": "您還沒有加入遊戲\n請直接"
                    },
                    {
                        "type": "span",
                        "text": " 輸入房號 ",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#2372b8"
                    },
                    {
                        "type": "span",
                        "text": "來加入\n或"
                    },
                    {
                        "type": "span",
                        "text": " 點擊下方按鈕 ",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#4b7a4e"
                    },
                    {
                        "type": "span",
                        "text": "來建立新遊戲"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "postback",
                        "label": "建立新遊戲",
                        "data": "@data"
                        },
                        "style": "primary",
                        "color": "#59915c"
                    }
                    ]
                }
                ],
                "spacing": "lg"
            }
            }"""
        template = template.replace(
            "@data", PostbackData(PostbackType.CreateGame).toFormatedJSON())
        return View("", FlexSendMessage(alt_text="請建立或加入遊戲", contents=json.loads(template, strict=False)))

    def joinGameFail():
        template = """{
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "image",
                        "url": "https://cdn-icons-png.flaticon.com/128/1828/1828665.png",
                        "size": "22px",
                        "flex": 1,
                        "gravity": "center"
                    },
                    {
                        "type": "text",
                        "text": "加入失敗",
                        "flex": 4,
                        "gravity": "center",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#c75858"
                    }
                    ],
                    "offsetEnd": "lg"
                },
                {
                    "type": "text",
                    "wrap": true,
                    "contents": [
                    {
                        "type": "span",
                        "text": "請重新輸入正確的房號\n或"
                    },
                    {
                        "type": "span",
                        "text": " 點擊下方按鈕 ",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#4b7a4e"
                    },
                    {
                        "type": "span",
                        "text": "來建立新遊戲"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "postback",
                        "label": "建立新遊戲",
                        "data": "@data"
                        },
                        "style": "primary",
                        "color": "#59915c"
                    }
                    ]
                }
                ],
                "spacing": "lg"
            }
            }"""
        template = template.replace(
            "@data", PostbackData(PostbackType.CreateGame).toFormatedJSON())
        return View("", FlexSendMessage(alt_text="加入遊戲失敗", contents=json.loads(template, strict=False)))

    def leavedGame():
        template = """{
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "image",
                        "url": "https://cdn-icons-png.flaticon.com/512/8333/8333895.png",
                        "size": "33px",
                        "flex": 1,
                        "gravity": "center",
                        "aspectMode": "cover"
                    },
                    {
                        "type": "text",
                        "flex": 4,
                        "gravity": "center",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#7a7a7a",
                        "text": "您已經退出遊戲"
                    }
                    ],
                    "offsetEnd": "lg"
                },
                {
                    "type": "text",
                    "wrap": true,
                    "contents": [
                    {
                        "type": "span",
                        "text": "請"
                    },
                    {
                        "type": "span",
                        "text": " 輸入房號 ",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#2372b8"
                    },
                    {
                        "type": "span",
                        "text": "來加入遊戲\n或"
                    },
                    {
                        "type": "span",
                        "text": " 點擊下方按鈕 ",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#4b7a4e"
                    },
                    {
                        "type": "span",
                        "text": "來建立新遊戲"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "postback",
                        "label": "建立新遊戲",
                        "data": "@data"
                        },
                        "style": "primary",
                        "color": "#59915c"
                    }
                    ]
                }
                ],
                "spacing": "lg"
            }
            }"""
        template = template.replace(
            "@data", PostbackData(PostbackType.CreateGame).toFormatedJSON())
        return View("", FlexSendMessage(alt_text="您已經退出遊戲", contents=json.loads(template, strict=False)))

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
        message["header"] = ViewFactory._getGameHeader(argument, id, True)
        return View(id, FlexSendMessage(alt_text="您確定要退出嗎?", contents=message))

    def askAmount(argument: ConsoleArgument, text: str):
        template = """{
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "您要@Text多少錢？",
                    "wrap": true
                }
                ],
                "paddingBottom": "xxl",
                "paddingAll": "xxl"
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
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://cdn-icons-png.flaticon.com/512/657/657059.png",
                            "size": "15px",
                            "align": "end"
                        },
                        {
                            "type": "text",
                            "text": "取消",
                            "weight": "bold",
                            "align": "start",
                            "flex": 2
                        }
                        ],
                        "action": {
                        "type": "postback",
                        "data": "@Console"
                        },
                        "spacing": "md",
                        "alignItems": "center",
                        "width": "100px",
                        "paddingStart": "lg",
                        "paddingEnd": "md"
                    }
                    ],
                    "margin": "xl",
                    "paddingEnd": "md",
                    "paddingStart": "md",
                    "justifyContent": "center"
                }
                ],
                "paddingTop": "none"
            }
        }"""

        id = str(uuid.uuid4())
        template = template.replace("@Text", text)
        template = template.replace(
            "@Console", PostbackData(PostbackType.Console, id).toFormatedJSON())
        message = json.loads(template, strict=False)
        message["header"] = ViewFactory._getGameHeader(argument, id)

        return View(id,  FlexSendMessage(
            alt_text=f"您要{text}多少錢？",
            contents=message,
            quick_reply=QuickReply([
                QuickReplyButton(action=MessageAction(
                    label="2000", text="2000")),
                QuickReplyButton(action=MessageAction(
                    label="1000", text="1000")),
                QuickReplyButton(action=MessageAction(
                    label="500", text="500")),
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
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    ],
                    "margin": "lg",
                    "spacing": "md"
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
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://cdn-icons-png.flaticon.com/512/657/657059.png",
                            "size": "15px",
                            "align": "end"
                        },
                        {
                            "type": "text",
                            "text": "取消",
                            "weight": "bold",
                            "align": "start",
                            "flex": 2
                        }
                        ],
                        "action": {
                        "type": "postback",
                        "data": "@Console"
                        },
                        "spacing": "md",
                        "alignItems": "center",
                        "width": "100px",
                        "paddingStart": "lg",
                        "paddingEnd": "md"
                    }
                    ],
                    "margin": "xl",
                    "paddingEnd": "md",
                    "paddingStart": "md",
                    "justifyContent": "center"
                }
                ],
                "paddingTop": "none"
            }
        }"""
        id = str(uuid.uuid4())
        message = json.loads(template, strict=False)
        message["header"] = ViewFactory._getGameHeader(argument)
        for playerId, playerName in players.items():
            message["body"]["contents"][1]["contents"].append(
                ButtonComponent(
                    action=PostbackAction(
                        label=playerName, 
                        data=PostbackData(PostbackType.SelectTransferTarget, id, playerId).toFormatedJSON()),
                    style="primary",
                    color="#5a76ad"))
        return View(id, FlexSendMessage(alt_text="請選擇匯款對象", contents=message))

    def inputError(argument: ConsoleArgument):
        template = """{
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "輸入錯誤，請重新輸入",
                    "wrap": true
                }
                ],
                "paddingBottom": "xxl",
                "paddingAll": "xxl"
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
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://cdn-icons-png.flaticon.com/512/657/657059.png",
                            "size": "15px",
                            "align": "end"
                        },
                        {
                            "type": "text",
                            "text": "取消",
                            "weight": "bold",
                            "align": "start",
                            "flex": 2
                        }
                        ],
                        "action": {
                        "type": "postback",
                        "data": "@Console"
                        },
                        "spacing": "md",
                        "alignItems": "center",
                        "width": "100px",
                        "paddingStart": "lg",
                        "paddingEnd": "md"
                    }
                    ],
                    "margin": "xl",
                    "paddingEnd": "md",
                    "paddingStart": "md",
                    "justifyContent": "center"
                }
                ],
                "paddingTop": "none"
            }
        }"""

        id = str(uuid.uuid4())
        template = template.replace(
            "@Console", PostbackData(PostbackType.Console, id).toFormatedJSON())
        message = json.loads(template, strict=False)
        message["header"] = ViewFactory._getGameHeader(argument, id)

        return View(id,  FlexSendMessage(alt_text=f"輸入錯誤，請重新輸入", contents=message))

    def OperateSuccess(argument: ConsoleArgument, text: str, gameLogId: str):
        id = str(uuid.uuid4())
        view = ViewFactory.Console(argument, text=text, id=id)
        message = view.message.contents
        message.contents[0].body.layout = "horizontal"
        message.contents[0].body.paddingEnd = "lg"
        message.contents[0].body.alignItems = "center"
        message.contents[0].body.contents[0].flex = 3
        message.contents[0].body.contents.append(ButtonComponent(
            style="primary",
            color="#a4a8b0",
            action=PostbackAction(label="撤銷", data=PostbackData(PostbackType.Rollback, id, {
                "gameLogId": gameLogId
            }).toFormatedJSON())
        ))
        return view

    def _getGameHeader(argument: ConsoleArgument, id="", hideLeave=False):
        template = """{
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "@gameId",
                            "size": "md",
                            "align": "center",
                            "gravity": "center",
                            "weight": "bold",
                            "color": "#103252"
                        }
                        ],
                        "margin": "xl",
                        "backgroundColor": "#c0d9f0",
                        "maxWidth": "50px"
                    },
                    {
                        "type": "text",
                        "text": "@username",
                        "weight": "bold",
                        "color": "#396996",
                        "margin": "md",
                        "align": "center",
                        "offsetEnd": "md"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "餘額：",
                            "size": "md",
                            "align": "center",
                            "gravity": "center",
                            "offsetTop": "1px",
                            "color": "#5e8c5a",
                            "weight": "bold",
                            "offsetStart": "sm"
                        }
                        ],
                        "margin": "xl",
                        "maxWidth": "50px"
                    },
                    {
                        "type": "text",
                        "text": "@balance",
                        "margin": "md",
                        "weight": "bold",
                        "color": "#5e8c5a",
                        "align": "center",
                        "offsetEnd": "md"
                    }
                    ],
                    "margin": "sm"
                }
                ],
                "alignItems": "center",
                "flex": 9,
                "offsetEnd": "15px"
            },
            {
                "type": "filler"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "image",
                    "url": "https://cdn-icons-png.flaticon.com/512/402/402718.png",
                    "size": "25px"
                },
                {
                    "type": "text",
                    "text": "退出",
                    "align": "center",
                    "size": "xxs",
                    "weight": "bold"
                }
                ],
                "spacing": "sm",
                "cornerRadius": "xl",
                "action": {
                "type": "postback",
                "data": "@LeaveConfirm"
                },
                "position": "absolute",
                "paddingAll": "20px",
                "paddingTop": "23px"
            }
            ],
            "alignItems": "center",
            "justifyContent": "flex-end"
        }"""
        template = template.replace("@gameId", argument.gameId)
        template = template.replace("@username", argument.username)
        template = template.replace(
            "@balance", "{:,}".format(argument.balance))
        template = template.replace(
            "@LeaveConfirm", PostbackData(PostbackType.LeaveConfirm, id).toFormatedJSON())
        message = json.loads(template, strict=False)
        if hideLeave:
            del message["contents"][2]
        return message

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
                    ],
                    "paddingBottom": "xxl",
                    "paddingAll": "xxl"
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
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://cdn-icons-png.flaticon.com/512/3135/3135673.png",
                                "size": "25px"
                            },
                            {
                                "type": "text",
                                "text": "領錢",
                                "align": "center",
                                "weight": "bold"
                            }
                            ],
                            "spacing": "sm",
                            "paddingAll": "sm",
                            "paddingTop": "lg",
                            "cornerRadius": "xl",
                            "action": {
                            "type": "postback",
                            "data": "@Earn"
                            },
                            "backgroundColor": "#d1ded1"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://cdn-icons-png.flaticon.com/512/3141/3141818.png",
                                "size": "25px"
                            },
                            {
                                "type": "text",
                                "text": "繳錢",
                                "align": "center",
                                "weight": "bold"
                            }
                            ],
                            "spacing": "sm",
                            "paddingAll": "sm",
                            "backgroundColor": "#ffd7d1",
                            "paddingTop": "lg",
                            "cornerRadius": "xl",
                            "action": {
                            "type": "postback",
                            "data": "@Pay"
                            }
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://cdn-icons-png.flaticon.com/512/1570/1570917.png",
                                "size": "25px"
                            },
                            {
                                "type": "text",
                                "text": "匯錢",
                                "align": "center",
                                "weight": "bold"
                            }
                            ],
                            "spacing": "sm",
                            "paddingAll": "sm",
                            "paddingTop": "lg",
                            "cornerRadius": "xl",
                            "action": {
                            "type": "postback",
                            "data": "@Transfer"
                            },
                            "backgroundColor": "#bbe0f2"
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
                            "style": "primary",
                            "color": "#e07e5a"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "postback",
                            "label": "命運",
                            "data": "@Destiny"
                            },
                            "style": "primary",
                            "color": "#5a76ad"
                        }
                        ],
                        "spacing": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://cdn-icons-png.flaticon.com/512/3024/3024605.png",
                                "size": "25px",
                                "align": "start",
                                "action": {
                                "type": "postback",
                                "label": "action",
                                "data": "@UserInfo"
                                },
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "我的財產",
                                "flex": 3,
                                "weight": "bold",
                                "size": "xs"
                            }
                            ],
                            "alignItems": "center",
                            "action": {
                            "type": "postback",
                            "data": "@UserInfo"
                            }
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://cdn-icons-png.flaticon.com/512/3606/3606497.png",
                                "size": "25px",
                                "align": "end",
                                "action": {
                                "type": "postback",
                                "label": "action",
                                "data": "@UserInfo"
                                },
                                "flex": 3
                            },
                            {
                                "type": "text",
                                "text": "購地",
                                "flex": 1,
                                "weight": "bold",
                                "size": "xs",
                                "align": "end"
                            }
                            ],
                            "alignItems": "center",
                            "action": {
                            "type": "postback",
                            "data": "@BuyLand"
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
            "@UserInfo", PostbackData(PostbackType.UserInfo, id).toFormatedJSON())
        message = json.loads(template, strict=False)
        message["contents"][0]["header"] = ViewFactory._getGameHeader(
            argument, id)
        if len(argument.logs) > 0:
            message["contents"].append(
                ViewFactory._getGameLogBubble(argument.logs, id))
        for bubble in bubbles:
            message["contents"].append(bubble)
        alt_text = text
        if text != None:
            template = message["contents"][0]["body"]["contents"][0]["text"] = text
        else:
            message["contents"][0]["body"]["contents"] = []
            alt_text = "控制面板"
        return View(id, FlexSendMessage(alt_text=alt_text, contents=message))

    def _getGameLogBubble(logs: list[GameLog], id=""):
        template = """{
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "操作紀錄",
                    "weight": "bold",
                    "size": "xl",
                    "margin": "md"
                },
                {
                    "type": "image",
                    "url": "https://cdn-icons-png.flaticon.com/512/2618/2618245.png",
                    "position": "absolute",
                    "size": "30px",
                    "action": {
                    "type": "postback",
                    "data": "@Console"
                    },
                    "offsetTop": "20px",
                    "offsetEnd": "15px"
                }
                ],
                "paddingBottom": "none",
                "justifyContent": "flex-end"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "paddingTop": "md",
                "spacing": "md",
                "paddingEnd": "lg"
            }
        }"""
        template = template.replace(
            "@Console", PostbackData(PostbackType.Console, id).toFormatedJSON())
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

            message["body"]["contents"].append(
                BoxComponent(layout="horizontal", contents=[
                    BoxComponent(layout="vertical", flex=3, contents=[
                        TextComponent(text=log.name, size="sm", color="#666666", weight="bold", wrap=True),
                        TextComponent(text=str(log), size="sm", wrap=True, decoration="line-through" if log.canceled else "none")
                    ]),
                    TextComponent(
                        text=text,
                        size="sm", color="#929394", flex=1, gravity="bottom", margin="md", align="end"),
                ]))

        return message
