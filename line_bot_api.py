from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi

# 💬 回覆元件（訊息本體）
from linebot.v3.messaging.models import (
    TextMessage,
    StickerMessage,
    LocationMessage,
    FlexMessage,
    FlexContainer,
    FlexBubble,
    FlexCarousel,
    TemplateMessage
)

# 🧩 模板類型
from linebot.v3.messaging.models import (
    ImageCarouselTemplate,
    ImageCarouselColumn,
    ConfirmTemplate,
    ButtonsTemplate
)

# 🎯 Quick Reply 與 Action 按鈕
from linebot.v3.messaging.models import (
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    MessageAction
)

# 📩 API 用的 Request 類別
from linebot.v3.messaging.models import (
    ReplyMessageRequest
)

# 🔔 事件物件（Webhook Event）
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FollowEvent,
    UnfollowEvent,
    PostbackEvent
)

# ✅ Line Bot 配置（AccessToken & Secret）
configuration = Configuration(access_token='POCtRxqnCqAX7I/mawGAmUv6X3/hyREtOFTh0HnvsDLDWvuHCZWhfLb1/DPjK+nWs1XZhLc7/mel4OpTL77gSmmMKcZKPzm78prE9W1FIVwwIlKc+WnjVuyCOsh5f8LR8oJgiEhRj3n1FdL3oORT1gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f3ee2fd2c4344a3913de723ac053a3d1')

