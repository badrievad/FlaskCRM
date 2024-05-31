#!/bin/bash
# Устанавливаем переменные окружения
export FLASK_APP=app

# Запускаем приложение Flask
flask run --host=0.0.0.0 --port 8005 --debug

#gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 app:app
