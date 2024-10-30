from datetime import datetime

from flask import session
from flask_socketio import emit, join_room, leave_room

from app.deal_inside.models import DealSteps
from logger import logging

from .. import db, socketio

# Словарь для хранения сопоставления username и socket.id
user_sessions = {}


@socketio.on("join")
def on_join(data):
    username = data["username"]
    room = data["room"]
    if room:  # Проверяем, что комната не пустая
        logging.info(f"{username} подключился к комнате {room}.")
        join_room(room)
        emit(f"{username} подключился к комнате {room}.", to=room)
    else:
        logging.info("Ошибка: не удалось подключиться, комната не указана.")


@socketio.on("leave")
def on_leave(data):
    username = data["username"]
    room = data["room"]
    if room:
        leave_room(room)
        emit(f"{username} покинул комнату {room}.", to=room)
    else:
        logging.info("Ошибка: не удалось выйти, комната не указана.")


@socketio.on("update_data")
def handle_update(data):
    room = data["room"]
    if room:
        # Отправляем сообщение всем пользователям в комнате
        emit(data["message"], to=room)
    else:
        logging.info("Ошибка: не удалось отправить данные, комната не указана.")


@socketio.on("approve_step")
def approve_step(data):
    step = data["step"]
    username = session.get("username", "Anonymous")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deal = DealSteps.query.first()

    if step == "step1":
        deal.step1_approved = True
        deal.step1_time = time_now
        deal.step1_user = username
    elif step == "step2":
        deal.step2_approved = True
        deal.step2_time = time_now
        deal.step2_user = username

    if deal.step1_approved and deal.step2_approved:
        deal.step3_approved = True
        deal.step3_time = time_now
        deal.step3_user = username

    db.session.commit()

    emit(
        "update_steps",
        {
            "step1": {
                "approved": deal.step1_approved,
                "time": deal.step1_time,
                "user": deal.step1_user,
            },
            "step2": {
                "approved": deal.step2_approved,
                "time": deal.step2_time,
                "user": deal.step2_user,
            },
            "step3": {
                "approved": deal.step3_approved,
                "time": deal.step3_time,
                "user": deal.step3_user,
            },
        },
        broadcast=True,
    )


@socketio.on("revoke_step")
def revoke_step(data):
    step = data["step"]
    deal = DealSteps.query.first()

    if step == "step1":
        deal.step1_approved = False
        deal.step1_time = None
        deal.step1_user = None
    elif step == "step2":
        deal.step2_approved = False
        deal.step2_time = None
        deal.step2_user = None

    if not deal.step1_approved or not deal.step2_approved:
        deal.step3_approved = False
        deal.step3_time = None
        deal.step3_user = None

        db.session.commit()

        emit(
            "update_steps",
            {
                "step1": {
                    "approved": deal.step1_approved,
                    "time": deal.step1_time,
                    "user": deal.step1_user,
                },
                "step2": {
                    "approved": deal.step2_approved,
                    "time": deal.step2_time,
                    "user": deal.step2_user,
                },
                "step3": {
                    "approved": deal.step3_approved,
                    "time": deal.step3_time,
                    "user": deal.step3_user,
                },
            },
            broadcast=True,
        )

    db.session.commit()
