from .. import socketio, db

from datetime import datetime
from flask_socketio import emit, join_room
from flask import session
from app.deal.models import DealSteps
from logger import logging
from flask_login import current_user


# Словарь для хранения сопоставления username и socket.id
user_sessions = {}


@socketio.on("connect")
def handle_connect():
    username = session.get("username")
    if username:
        user_sessions[username] = current_user.login
        join_room(username)  # Присоединяем пользователя к комнате с его именем
        logging.info(f"User {username} connected with session ID {current_user.login}")


@socketio.on("disconnect")
def handle_disconnect():
    username = session.get("username")
    logging.info(f"User {username} disconnected")
    if username and username in user_sessions:
        del user_sessions[username]  # Удаляем запись при отключении
        logging.info(f"User {username} disconnected")


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
