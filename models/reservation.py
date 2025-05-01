
from datetime import datetime
from extensions import db

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    booking_service_category = db.Column(db.String(255), nullable=False)
    booking_service = db.Column(db.String(255), nullable=False)
    booking_datetime = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    is_cancelled = db.Column(db.Boolean, default=False)  # 新增取消狀態欄位
