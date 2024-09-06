#!/bin/env python
from app import create_app, socketio
from app.config import SOCKETIO_BACKEND

app = create_app(debug=True)

if __name__ == "__main__":
    socketio.run(app, port=8005, host="0.0.0.0", message_queue=SOCKETIO_BACKEND)
