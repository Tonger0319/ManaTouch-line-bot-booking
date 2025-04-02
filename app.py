from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, abort
from events.admin import *
from events.basic import *
from events.service import *
from extensions import db, migrate
from line_bot_api import *
from models.reservation import Reservation
from models.user import User
from urllib.parse import parse_qsl

app = Flask(__name__)
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.app=app
print("💡 Render DATABASE_URL:", os.environ.get('DATABASE_URL'))

db.init_app(app)
migrate.init_app(app,db)
with app.app_context():
    db.create_all()



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    message_text = str(event.message.text).lower()
    # 透過 MessagingApi 實例取得用戶資料
    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)
        profile = line_api.get_profile(event.source.user_id)



    user = User.query.filter(User.line_id == profile.user_id).first()
    if not user:
        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    #print(user.id)
    #print(user.line_id)
    #print(user.display_name)



    if message_text=='@關於我們':
        about_us_event(event)
    if message_text=='@營業據點':
        location_event(event)
    if message_text == '@預約服務':
        service_category_event(event)
    if message_text == '@我的預約':
        my_reservation_event(event)

    elif message_text.startswith('*'):
        if event.source.user_id not in ['U459e35a3aa5732fc5b08bded154ab07c']:#管理者line ID
            return
        if message_text in ['*data', '*d']:
            list_reservation_event(event)



@handler.add(PostbackEvent)
def handle_postback(event):

    data = dict(parse_qsl(event.postback.data))
    action = data.get('action')

    print("\n===== 📩 收到 Postback Event =====")
    print("✅ 原始 data:", event.postback.data)
    print("✅ 解析後 action:", action)
    print("✅ 其他資訊:")
    print("   - category:", data.get('category'))
    print("   - service_id:", data.get('service_id'))
    print("   - date:", data.get('date'))
    print("   - time:", data.get('time'))
    print("===================================\n")

    try:
        if action == 'service':
            print("👉 進入服務分類回覆 (service_event)")
            service_event(event)

        elif action == 'select_date':
            print("👉 進入日期選擇步驟 (service_select_date_event)")
            service_select_date_event(event)

        elif action == 'select_time':
            print("👉 進入時間選擇步驟 (service_select_time_event)")
            service_select_time_event(event)

        elif action == 'confirm':
            print("👉 進入預約確認步驟 (service_confirm_event)")
            service_confirm_event(event)

        elif action == 'confirmed':
            print("👉 預約已確認 (service_confirmed_event)")
            service_confirmed_event(event)

        elif action == 'cancel':
            print("👉 預約取消(service_cancel_event)")
            service_cancel_event(event)

        elif action == 'modify':
            print("👉 使用者選擇修改預約 (service_select_date_event)")
            service_select_date_event(event)

        else:
            print(f"⚠️ 未定義的 action: {action}")

    except Exception as e:
        print("❌ 發生錯誤：", str(e))


@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = """Hellow 您好，歡迎成為ManaTouch的好友!
我是ManaTouch 的小幫手

-想預約夏威夷按摩LomiLomi都可以直接跟我互動喔~
-也可以直接點選下方選單功能

-期待您的光臨! """

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=welcome_msg)]
            )
        )

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)




def send_reminders():
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    end_time = start_time + timedelta(days=1)

    reservations = Reservation.query.filter(
        Reservation.booking_datetime >= start_time,
        Reservation.booking_datetime < end_time,
        Reservation.is_canceled.is_(False)
    ).all()

    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)

        for reservation in reservations:
            user = User.query.get(reservation.user_id)
            if user:
                line_api.push_message(
                    to=user.line_id,
                    messages=[
                        TextMessage(text=f'🌞 提醒您：明天 {reservation.booking_datetime.strftime("%H:%M")} 有預約【{reservation.booking_service}】，期待與您見面 🌺')
                    ]
                )
                print(f"✅ 已推播提醒給 {user.display_name}")


with app.app_context():
    print("🚀 正在嘗試建立資料表...")
    db.create_all()
    print("✅ 資料表建立完成（如果尚未存在）")


# 啟用排程器
scheduler = BackgroundScheduler()
scheduler.add_job(send_reminders, 'cron', hour=10)  # 每天上午 10 點執行
scheduler.start()

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200


from flask import render_template
from models.reservation import Reservation
from extensions import db

@app.route("/admin/reservations")
def admin_reservations():
    reservations = Reservation.query.order_by(Reservation.date, Reservation.time).all()
    return render_template("admin_reservations.html", reservations=reservations)