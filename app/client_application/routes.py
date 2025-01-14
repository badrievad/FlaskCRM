from flask import jsonify

from . import client_application_bp
from ..config import CLIENT_APPLICATION_VERSION, CLIENT_APPLICATION_URL


@client_application_bp.route("/latest-version", methods=["GET"])
def latest_version():
    """
    Возвращает информацию о последней версии клиентского приложения.
    """
    return jsonify(
        {
            "version": CLIENT_APPLICATION_VERSION,  # Текущая версия на сервере
            "download_url": CLIENT_APPLICATION_URL,  # Ссылка на скачивание
        }
    )
