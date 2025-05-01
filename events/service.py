from line_bot_api import *
import datetime
from urllib.parse import parse_qsl

from extensions import db
from models.user import User
from models.reservation import Reservation



services = {
    1: {
        'category': 'Lomi按摩',
        'img_url': 'https://drive.google.com/uc?export=download&id=15ftd3m_rOX3Op_js9B5OCiz2a4KyQfXi',
        'title': 'LomiLomi按摩',
        'duration': '150min',
        'description': '夏威夷傳統療癒按摩，透過長且流動的手法，搭配Ho\'oponopono與呼吸法，讓身心達到平衡',
        'price': 3600,
        'post_url': 'https://www.instagram.com/manatouch_taipei/'
    },
    2: {
        'category': 'Lomi按摩',
        'img_url': 'https://drive.google.com/uc?export=download&id=1naYV7ySDy1PBTR9_smzchSu3xPfuKRYO',
        'title': '客製化lomi按摩（熟客）',
        'duration': '150min',
        'description': '視當天狀態提供不同形式的Lomi服務，並輔以與身體能量相應的精油',
        'price': 4000,
        'post_url': 'https://www.instagram.com/manatouch_taipei/'
    },
    3: {
        'category': '按摩調理',
        'img_url': 'https://drive.google.com/uc?export=download&id=1dOiR8rnSski88B7s8tEClN6bR4OXP2VY',
        'title': '熱石精油紓壓',
        'duration': '90min',
        'description': '「火山石」成份含有豐富礦物質及獨特的自然能量，溫熱觸感能活絡循環，鬆解疲勞感，舒緩肌肉緊繃',
        'price': 2000,
        'post_url': 'https://linecorp.com'
    },
    4: {
        'category': '臉部護理',
        'img_url': 'https://drive.google.com/uc?export=download&id=1j9k2ivv1D3DwthQABmiI-PLsn6pN7sIZ',
        'title': '粉刺淨化 + 深層保濕',
        'duration': '90min',
        'description': '臉部淨化李，粉刺淨化 + 深層保濕繃',
        'price': 1500,
        'post_url': 'https://linecorp.com'
    },

}


def get_service_id_from_name(service_name):
    for sid, service in services.items():
        full_name = f"{service['title']} {service['duration']}"
        if full_name == service_name:
            return sid
    return None



def service_category_event(event):
    carousel = TemplateMessage(
       alt_text='請選擇想服務的類別',
       template=ImageCarouselTemplate(
           columns=[
               ImageCarouselColumn(
                   image_url='https://drive.google.com/uc?export=download&id=1EH01UExdzrGCbA4v1GY8MbIrOmhRj1Vh',
                   action=PostbackAction(
                       label = 'Lomi按摩',
                       display_text="想了解LomiLomi按摩",
                       data='action=service&category=Lomi按摩'
                  )
               ),
               ImageCarouselColumn(
                   image_url='https://drive.google.com/uc?export=download&id=1ENqGaCjQJ2ORLKQ33KB3vv2lCnl1yGOc',
                   action=PostbackAction(
                       label ='魔法蠟燭',
                       display_text="購買魔法蠟燭",
                       data='action=service&category=魔法蠟燭'
                   )
               )
            ]
       )
    )
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[carousel]
            )
        )

def service_event(event):
    data = dict(parse_qsl(event.postback.data))
    category = data.get('category')

    bubbles = []

    for service_id in services:
        if services[service_id]['category'] == category:
            service = services[service_id]
            bubble_dict = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": service['img_url']
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": service['title'],
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "text",
                            "text": service['duration'],
                            "size": "md",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": service['description'],
                            "margin": "lg",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"NT$ {service['price']}",
                                    "wrap": True,
                                    "weight": "bold",
                                    "size": "xl",
                                    "flex": 0
                                }
                            ],
                            "margin": "xl"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "postback",
                                "label": "預約",
                                "data": f"action=select_date&service_id={service_id}",
                                "displayText": f"我想預約【{service['title']} {service['duration']}】"
                            },
                            "color": "#b28530"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "IG了解詳情",
                                "uri": service['post_url']
                            }
                        }
                    ]
                }
            }

            bubbles.append(FlexBubble.from_dict(bubble_dict))

    if not bubbles:
      print("❌ 找不到符合的服務項目，bubbles 為空！")
      return


    carousel = FlexCarousel(contents=bubbles)

    flex_message = FlexMessage(
        alt_text='請選擇預約項目',
        contents=carousel
     )

    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)
        line_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[flex_message]
            )
        )

def is_booked(user, booking_datetime):
    if user is None:
        print("⚠️ user is None，無法判斷是否已預約")
        return False

    reservation = Reservation.query.filter(
        Reservation.user_id == user.id,
        Reservation.is_cancelled.is_(False),
        Reservation.booking_datetime == booking_datetime
    ).first()

    return bool(reservation)



    if reservation:
        time_str = reservation.booking_datetime.strftime('%Y-%m-%d %H:%M')
        buttons_template_message = TemplateMessage(
            alt_text='您已經有預約了，是否需要取消?',
            template=ButtonsTemplate(
                title='您已經有預約了',
                text=f'{reservation.booking_service}\n預約時段: {time_str}',
                actions=[
                    PostbackAction(
                        label='我想取消預約',
                        display_text='確認，但我想取消預約',
                        data='action=cancel'
                    )
                ]
            )
        )

        with ApiClient(configuration) as api_client:
            MessagingApi(api_client).reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[buttons_template_message]
                )
            )

        print(f"🔁 使用者 {user.display_name} 已有預約，訊息已送出")
        return True
    else:
        return False


def service_select_date_event(event):

    user = User.query.filter(User.line_id == event.source.user_id).first()


    data = dict(parse_qsl(event.postback.data))
    service_id = data.get('service_id')

    weekday_string = {
        0: '一',
        1: '二',
        2: '三',
        3: '四',
        4: '五',
        5: '六',
        6: '日',
    }

    business_day = [0,1, 2, 3, 4, 5, 6] #星期一到日

    today = datetime.date.today()
    actions = []

    for x in range(1, 11):
        day = today + datetime.timedelta(days=x)

        if day.weekday() in business_day:
            label = f'{day} ({weekday_string[day.weekday()]})'
            actions.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        data=f"action=select_time&service_id={service_id}&date={day}",
                        display_text=f"我想預約 {label}"
                    )
                )
            )

    message = TextMessage(
        text='請問要預約哪一天？',
        quick_reply=QuickReply(items=actions)
    )

    try:
        with ApiClient(configuration) as api_client:
            MessagingApi(api_client).reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[message]
                )
            )
        print("✅ 日期 Quick Reply 已送出")
    except Exception as e:
        print("❌ 發送 Quick Reply 失敗：", str(e))

def service_select_time_event(event):

    data = dict(parse_qsl(event.postback.data))

    available_time = ['10:00', '14:00', '18:00']

    quick_reply_buttons = []

    for time in available_time:
        quick_reply_buttons.append(
            QuickReplyItem(
                action=PostbackAction(
                    label=time,
                    display_text=f"我想預約 {time}",
                    data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'
                )
            )
        )

    text_message = TextMessage(
        text='請問要預約哪個時段?',
        quick_reply=QuickReply(items=quick_reply_buttons)
    )
    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)
        line_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[text_message]
            )
        )
    print("✅ 時段 Quick Reply 已送出")


def service_confirm_event(event):

    data = dict(parse_qsl(event.postback.data))
    booking_service = services[int(data['service_id'])]

    user = User.query.filter(User.line_id == event.source.user_id).first()
    booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')

    if is_booked(user, booking_datetime):
        with ApiClient(configuration) as api_client:
            MessagingApi(api_client).reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="⚠️ 您已經預約了這個時段喔，請選擇不同的時間 😊")]
                )
            )
        return

    confirm_template_message = TemplateMessage(
        alt_text='請確認預約項目',
        template=ConfirmTemplate(
            text=f'您即將預約\n\n{booking_service["title"]} {booking_service["duration"]}\n預約時段: {data["date"]} {data["time"]}\n\n確認沒問題請按【確定】',
            actions=[
                PostbackAction(
                    label='確定',
                    display_text='確認沒問題!',
                    data=f'action=confirmed&service_id={data["service_id"]}&date={data["date"]}&time={data["time"]}'
                ),
                MessageAction(
                    label='重新預約',
                    text='我想重新預約'
                )
            ]
        )
    )
    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[confirm_template_message]
            )
        )




def service_confirmed_event(event):
    data = dict(parse_qsl(event.postback.data))

    booking_service = services[int(data['service_id'])]
    booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')

    user = User.query.filter(User.line_id == event.source.user_id).first()

    reservation = Reservation(
        user_id=user.id,
        booking_service_category=booking_service["category"],
        booking_service=f'{booking_service["title"]} {booking_service["duration"]}',
        booking_datetime=booking_datetime
    )

    db.session.add(reservation)
    db.session.commit()

    try:
        with ApiClient(configuration) as api_client:
            MessagingApi(api_client).reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text="沒問題! 感謝您的預約，我已經幫你預約成功了喔，到時候見!")
                    ]
                )
            )
        print("✅ 預約成功並已回覆用戶")
    except Exception as e:
        print("❌ 發送預約成功訊息失敗：", str(e))


def service_cancel_event(event):

    user = User.query.filter(User.line_id == event.source.user_id).first()
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_cancelled.is_(False),
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
    if reservation:
        reservation.is_cancelled = True

        db.session.add(reservation)
        db.session.commit()

        with ApiClient(configuration) as api_client:
            MessagingApi(api_client).reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text='您的預約已經幫你取消了')
                    ]
                )
            )
        print(f"✅ 使用者 {user.display_name} 的預約已取消")
    else:
        with ApiClient(configuration) as api_client:
            MessagingApi(api_client).reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text='您目前沒有預約喔')
                    ]
                )
            )
        print("✅ 該使用者沒有預約記錄")

def my_reservation_event(event):
    user = User.query.filter(User.line_id == event.source.user_id).first()

    reservations = Reservation.query.filter(
        Reservation.user_id == user.id,
        Reservation.is_cancelled.is_(False),
        Reservation.booking_datetime > datetime.datetime.now()
    ).order_by(Reservation.booking_datetime.asc()).all()

    if not reservations:
        with ApiClient(configuration) as api_client:
            MessagingApi(api_client).reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="您目前沒有任何預約喔～")]
                )
            )
        return

    bubbles = []
    for res in reservations:
        time_str = res.booking_datetime.strftime('%Y-%m-%d %H:%M')
        service_id = get_service_id_from_name(res.booking_service)

        bubble = FlexBubble.from_dict({
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{res.booking_service}",
                        "weight": "bold",
                        "size": "xl",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": f"預約時間: {time_str}",
                        "margin": "md",
                        "wrap": True
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "spacing": "md",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#b28530",
                        "action": {
                            "type": "postback",
                            "label": "修改預約",
                            "displayText": "我想修改預約",
                            "data": f"action=modify&service_id={service_id}"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "action": {
                            "type": "postback",
                            "label": "取消預約",
                            "displayText": "我想取消預約",
                            "data": "action=cancel"
                        }
                    }
                ]
            }
        })
        bubbles.append(bubble)

    carousel = FlexCarousel(contents=bubbles)
    flex_message = FlexMessage(
        alt_text='您的預約清單如下',
        contents=carousel
    )

    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[flex_message]
            )
        )