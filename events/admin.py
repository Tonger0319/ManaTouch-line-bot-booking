from line_bot_api import *

from models.reservation import Reservation
import datetime


def list_reservation_event(event):
    reservations = Reservation.query.filter(Reservation.is_canceled.is_(False),
                                            Reservation.booking_datetime > datetime.datetime.now(),
                                            ).order_by(Reservation.booking_datetime.asc()).all()

    reservation_data_text = '## 預約名單: ## \n\n'

    for reservation in reservations:
        reservation_data_text += (
    f"預約日期: {reservation.booking_datetime}\n"
    f"預約服務: {reservation.booking_service}\n"
    f"姓名: {reservation.user.display_name}\n\n"
)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reservation_data_text)]
            )
        )

