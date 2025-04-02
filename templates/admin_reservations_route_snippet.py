
from flask import Flask, render_template
from models.reservation import Reservation
from extensions import db

@app.route("/admin/reservations")
def admin_reservations():
    reservations = Reservation.query.order_by(Reservation.date, Reservation.time).all()
    return render_template("admin_reservations.html", reservations=reservations)
