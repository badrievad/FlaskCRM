from flask import session
from flask_login import current_user
from flask_socketio import join_room

from logger import logging

from .. import socketio

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
