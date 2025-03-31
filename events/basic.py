from line_bot_api import *


def about_us_event(event):
    emoji = [
        {
            "index": 0,
            "productId": "5ac21184040ab15980c9b43a",
            "emojiId": "225"
        }
    ]
    about_text = '''$ManaTouch觸心能量
Mana 在夏威夷語代表生命、陽性能量

按摩師Kai提供夏威夷傳統療癒LomiLomi按摩
透過海浪般長且流動的手法
清理不屬於身體的能量

並在過程加入
夏威夷療癒寬恕系統Ho'oponopono
讓您在呼吸中感受釋放與平靜

Kai是經夏威夷權威大師Wayne Kealohi Powell 認證的lomilomi男療癒師

希望透過雙手讓您在ManaTouch

感受身體聲音，找回身心平衡。'''

    messages = [
        TextMessage(text=about_text, emojis=emoji),
        StickerMessage(package_id="11539", sticker_id="52114110")
    ]

# 統一在最後回傳訊息
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
              reply_token= event.reply_token,
              messages=messages
            )
         )


def location_event(event):
    location_message = LocationMessage(
        title='ManaTouch 觸心能量',
        address='106台北市大安區敦化南路一段177巷(捷運忠孝敦化站)',
        latitude=25.04342000653536,
        longitude=121.5513052693149
    )

    messages = [location_message]

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages
            )
        )