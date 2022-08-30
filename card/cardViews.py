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
            "https://thumbs.dreamstime.com/b/bomber-plane-drops-bomb-sketch-engraving-vector-illustration-scratch-board-style-imitation-hand-drawn-image-bomber-plane-drops-159425073.jpg",
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
            "https://thumbs.dreamstime.com/b/bomber-plane-drops-bomb-sketch-engraving-vector-illustration-scratch-board-style-imitation-hand-drawn-image-bomber-plane-drops-159425073.jpg",
            "命運",
            "外星人俘虜",
            "被外星人俘虜，暫停行動一回合(可以收過路費)")

        id = str(uuid.uuid4())
        return View(id, FlexSendMessage(alt_text="[命運] 外星人俘虜", contents=message))

    def goToJail(argument: ConsoleArgument):
        message = CardViewFactory._cardTemplate(
            argument,
            "https://thumbs.dreamstime.com/b/bomber-plane-drops-bomb-sketch-engraving-vector-illustration-scratch-board-style-imitation-hand-drawn-image-bomber-plane-drops-159425073.jpg",
            "命運",
            "牢底坐穿",
            "立刻去坐牢")

        id = str(uuid.uuid4())
        return View(id, FlexSendMessage(alt_text="[命運] 牢底坐穿", contents=message))

    def stockHit(argument: ConsoleArgument):
        pass

    def stockHitResultContinuable(argument: ConsoleArgument, text: str, times: int):
        pass

    def stockHitResultEnd(argument: ConsoleArgument, text: str):
        pass

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
