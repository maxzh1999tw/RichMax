import json
import uuid
from linebot.models import *

from views import *


class CardViewFactory(ViewFactory):
    def shootDownFighter(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://thumbs.dreamstime.com/b/bomber-plane-drops-bomb-sketch-engraving-vector-illustration-scratch-board-style-imitation-hand-drawn-image-bomber-plane-drops-159425073.jpg",
            "命運",
            "擊落戰鬥機",
            "擊落戰鬥機，得 $2000")

        footer = '''{
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "領取獎勵",
                        "data": "@data"
                    }
                }
            ]
        }'''

        id = str(uuid.uuid4())
        footer = footer.replace("@data", PostbackData(PostbackType.Destiny,
                                                      id, {"name": "擊落戰鬥機"}).toFormatedJSON())
        message["footer"] = json.loads(footer, strict=False)
        return View(id, FlexSendMessage(alt_text="[命運] 擊落戰鬥機", contents=message))

    def payTuition(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://pic.pimg.tw/stock2012/1407218694-550000070.jpg",
            "命運",
            "繳學費",
            "繳學費，失去 $800")

        footer = '''{
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "繳錢",
                        "data": "@data"
                    }
                }
            ]
        }'''

        id = str(uuid.uuid4())
        footer = footer.replace("@data", PostbackData(PostbackType.Destiny,
                                                      id, {"name": "繳學費"}).toFormatedJSON())
        message["footer"] = json.loads(footer, strict=False)
        return View(id, FlexSendMessage(alt_text="[命運] 繳學費", contents=message))

    def capturedByAliens(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://cdn.dribbble.com/users/4427600/screenshots/13960230/media/b39e1a569334f0cfb17ca84a5d258cdb.png?compress=1&resize=400x300&vertical=top",
            "命運",
            "外星人俘虜",
            "被外星人俘虜，暫停行動一回合(可以收過路費)")

        return View("", FlexSendMessage(alt_text="[命運] 外星人俘虜", contents=message))

    def goToJail(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://media.istockphoto.com/vectors/stressed-businessman-sitting-in-the-jail-vector-id827832778?k=20&m=827832778&s=612x612&w=0&h=1iScEQ8PV77S6lkOVyaQoHKHZoH79luBrUSWGlHEDeU=",
            "命運",
            "牢底坐穿",
            "立刻去坐牢")

        return View("", FlexSendMessage(alt_text="[命運] 牢底坐穿", contents=message))

    def stockHit(argument: ConsoleArgument, times: int, text=""):
        template = '''{
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://gia-invest.com/wp-content/uploads/2019/01/entrepreneur-1340649_1280.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
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
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": "機會",
                                "size": "md",
                                "margin": "none",
                                "align": "center",
                                "gravity": "center"
                            }
                            ],
                            "backgroundColor": "#b3f2e5",
                            "cornerRadius": "xl",
                            "paddingAll": "xs"
                        }
                        ],
                        "cornerRadius": "lg",
                        "justifyContent": "center",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": "股票當沖",
                        "weight": "bold",
                        "size": "xl",
                        "flex": 4
                    }
                    ],
                    "spacing": "md",
                    "alignItems": "center",
                    "justifyContent": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "您還有 @times 次當沖機會",
                        "weight": "bold",
                        "color": "#949494"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": "擲一顆骰子進行判定：",
                        "wrap": true,
                        "contents": [],
                        "margin": "lg"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
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
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Dice-1.svg/120px-Dice-1.svg.png",
                                "size": "20px",
                                "flex": 1,
                                "align": "start"
                            },
                            {
                                "type": "text",
                                "text": "得 $1000",
                                "color": "#e64b17",
                                "contents": [],
                                "flex": 4
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Dice-2-b.svg/120px-Dice-2-b.svg.png",
                                "size": "20px",
                                "flex": 1,
                                "align": "start"
                            },
                            {
                                "type": "text",
                                "text": "扣 $200",
                                "color": "#1a9c11",
                                "contents": [],
                                "flex": 4
                            }
                            ]
                        }
                        ],
                        "margin": "md"
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
                                "size": "20px",
                                "flex": 1,
                                "align": "start",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Dice-3-b.svg/120px-Dice-3-b.svg.png"
                            },
                            {
                                "type": "text",
                                "text": "扣 $300",
                                "color": "#1a9c11",
                                "contents": [],
                                "flex": 4
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Dice-4.svg/120px-Dice-4.svg.png",
                                "size": "20px",
                                "flex": 1,
                                "align": "start"
                            },
                            {
                                "type": "text",
                                "text": "得 $400",
                                "color": "#e64b17",
                                "contents": [],
                                "flex": 4
                            }
                            ]
                        }
                        ],
                        "margin": "md"
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
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Dice-5-b.svg/120px-Dice-5-b.svg.png",
                                "size": "20px",
                                "flex": 1,
                                "align": "start"
                            },
                            {
                                "type": "text",
                                "text": "扣 $500",
                                "color": "#1a9c11",
                                "contents": [],
                                "flex": 4
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "image",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Dice-6-b.svg/120px-Dice-6-b.svg.png",
                                "size": "20px",
                                "flex": 1,
                                "align": "start"
                            },
                            {
                                "type": "text",
                                "text": "扣 $600",
                                "color": "#1a9c11",
                                "contents": [],
                                "flex": 4
                            }
                            ]
                        }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "請選擇您骰到的數字",
                        "weight": "bold",
                        "color": "#7d7d7d",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Dice-1.svg/120px-Dice-1.svg.png",
                            "action": {
                            "type": "postback",
                            "data": "@data1"
                            },
                            "size": "xs"
                        },
                        {
                            "type": "image",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Dice-2-b.svg/120px-Dice-2-b.svg.png",
                            "action": {
                            "type": "postback",
                            "data": "@data2"
                            },
                            "size": "xs"
                        },
                        {
                            "type": "image",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Dice-3-b.svg/120px-Dice-3-b.svg.png",
                            "action": {
                            "type": "postback",
                            "data": "@data3"
                            },
                            "size": "xs"
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
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Dice-4.svg/120px-Dice-4.svg.png",
                            "action": {
                            "type": "postback",
                            "data": "@data4"
                            },
                            "size": "xs"
                        },
                        {
                            "type": "image",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Dice-5-b.svg/120px-Dice-5-b.svg.png",
                            "action": {
                            "type": "postback",
                            "data": "@data5"
                            },
                            "size": "xs"
                        },
                        {
                            "type": "image",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Dice-6-b.svg/120px-Dice-6-b.svg.png",
                            "action": {
                            "type": "postback",
                            "data": "@data6"
                            },
                            "size": "xs"
                        }
                        ],
                        "spacing": "md",
                        "margin": "xxl"
                    }
                    ],
                    "margin": "md",
                    "spacing": "md"
                }
                ]
            }
            }'''
        id = str(uuid.uuid4())
        template = template.replace("@times", str(times))
        for i in range(1, 7):
            template = template.replace(f"@data{i}", PostbackData(PostbackType.Chance,
                                                                  id, {"name": "股票當沖", "dice": i, "times": times}).toFormatedJSON())
        message = json.loads(template, strict=False)
        message["header"] = ViewFactory._getGameHeader(argument)

        if text != "":
            message["body"]["contents"][1]["contents"].insert(
                0, TextComponent(text, size="lg", color="#17061f", weight="bold", wrap=True))

        return View(id, FlexSendMessage(alt_text="[機會] 股票當沖", contents=message))

    def tripleDice(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://www.yunsanmotors.com/wp-content/uploads/2017/08/DSC_6013-25-1024x684.jpg",
            "機會",
            "豪華坐駕",
            "下一回合使用三顆骰子")
        return View("", FlexSendMessage(alt_text="[機會] 豪華坐駕", contents=message))

    def urbanRenewal(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://img95.699pic.com/photo/30677/6821.jpg_wh300.jpg",
            "機會",
            "都更協調會",
            "若所有玩家同意\n則每人可各蓋一棟房\n若無法達成共識\n則你選擇自己的一棟房子拆掉")
        return View("", FlexSendMessage(alt_text="[機會] 都更協調會", contents=message))

    def notGuilty(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://pic.52112.com/20190724/1/ALUXPX5SVB_small.jpg",
            "機會",
            "有關係沒關係",
            "獲得一張出獄許可證")
        return View("", FlexSendMessage(alt_text="[機會] 有關係沒關係", contents=message))

    def goToStation(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://freepikpsd.com/file/2020/06/train-station-cartoon-png.png",
            "機會",
            "公共運輸",
            "移動到任一車站，並進行行動")
        message["body"]["contents"][1]["contents"].append(TextComponent(
            text="行動: 購地、蓋房、或繳交過路費等", color="#969595", weight="bold", wrap=True))

        return View("", FlexSendMessage(alt_text="[機會] 公共運輸", contents=message))

    def forwardOrBackward(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://img95.699pic.com/xsj/00/mw/jq.jpg!/fh/300",
            "機會",
            "進退有據",
            "骰一顆骰子並自由決定前進或後退與骰出點數相同的格數")

        return View("", FlexSendMessage(alt_text="[機會] 進退有據", contents=message))
    
    def wholeLife(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://img-qn.51miz.com/preview/element/00/01/13/40/E-1134061-40B25517.jpg",
            "機會",
            "儲蓄險",
            "繳1000元，下次回到起點時額外獲得2000元")

        return View("", FlexSendMessage(alt_text="[機會] 儲蓄險", contents=message))

    def excessInsurance(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://img-qn.51miz.com/preview/element/00/01/13/40/E-1134061-40B25517.jpg",
            "機會",
            "超額保險",
            "繳交400元，下次過路費高於800元時由保險公司代繳")

        return View("", FlexSendMessage(alt_text="[機會] 超額保險", contents=message))

    def takeMeAway(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://upload.shejihz.com/wp-content/uploads/2020/11/ee819a54a933444fce9d0a14bbb7e522.jpg",
            "機會",
            "一起走",
            "傳送到任一玩家身邊")

        return View("", FlexSendMessage(alt_text="[機會] 一起走", contents=message))

    def youGoToJail(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://media.istockphoto.com/vectors/stressed-businessman-sitting-in-the-jail-vector-id827832778?k=20&m=827832778&s=612x612&w=0&h=1iScEQ8PV77S6lkOVyaQoHKHZoH79luBrUSWGlHEDeU=",
            "機會",
            "沒關係有關係",
            "指定一名玩家去坐牢，出獄時須給對方1000元")

        return View("", FlexSendMessage(alt_text="[機會] 沒關係有關係", contents=message))

    def giveLand(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://i.ytimg.com/vi/jL3izdtmBnI/maxresdefault.jpg",
            "機會",
            "施比受更有福",
            "地產最多者需贈與你一塊地，若你就是地產最多者，則給地產最少者一塊地，若有地產最少者超過一名，則取餘額最少者")

        return View("", FlexSendMessage(alt_text="[機會] 施比受更有福", contents=message))

    def fixHouse(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://img95.699pic.com/photo/30089/8321.jpg_wh860.jpg",
            "機會",
            "莫拉克風災",
            "所有玩家皆須修理房屋，一棟 $250，旅館 $1000")

        return View("", FlexSendMessage(alt_text="[機會] 莫拉克風災", contents=message))

    def changePosition(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://pic1.xuehuaimg.com/proxy/baijia/https://f10.baidu.com/it/u=714137997,695336803&fm=173&app=49&f=JPEG?w=580&h=292&s=8272C2255A01494F8E392BF30300C026&access=215967316",
            "機會",
            "天手力",
            "與任一玩家交換位置")

        return View("", FlexSendMessage(alt_text="[機會] 天手力", contents=message))

    def antiChance(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://weproclaimhim.com/wp-content/uploads/2017/12/171216-1.jpg",
            "機會",
            "不給機會",
            "老天爺不給你任何機會，什麼事都不會改變")

        return View("", FlexSendMessage(alt_text="[沒有機會] 不給機會", contents=message))

    def _cardTemplate(argument: ConsoleArgument, imgUrl: str, typeName: str, title: str, content: str):
        template = '''{
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "@ImgUrl",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
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
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "@TypeName",
                                            "size": "md",
                                            "margin": "none",
                                            "align": "center",
                                            "gravity": "center"
                                        }
                                    ],
                                    "backgroundColor": "#b3f2e5",
                                    "cornerRadius": "xl",
                                    "paddingAll": "xs"
                                }
                            ],
                            "cornerRadius": "lg",
                            "justifyContent": "center",
                            "flex": 1
                        },
                            {
                                "type": "text",
                                "text": "@Title",
                                "weight": "bold",
                                "size": "xl",
                                "flex": 4
                            }
                        ],
                        "spacing": "md",
                        "alignItems": "center",
                        "justifyContent": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "@Content",
                                "wrap": true
                            }
                        ]
                    }
                ]
            }
        }'''
        template = template.replace("@ImgUrl", imgUrl)
        template = template.replace("@TypeName", typeName)
        template = template.replace("@Title", title)
        template = template.replace("@Content", content)
        message = json.loads(template, strict=False)
        message["header"] = ViewFactory._getGameHeader(argument)
        return message
