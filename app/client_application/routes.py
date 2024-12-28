from flask import jsonify

from . import client_application_bp


@client_application_bp.route("/latest-version", methods=["GET"])
def latest_version():
    """
    Возвращает информацию о последней версии клиентского приложения.
    """
    return jsonify(
        {
            "version": "1.0.0",  # Текущая версия на сервере
            "download_url": "https://example.com/downloads/client_app_v1.1.0.exe",  # Ссылка на скачивание
        }
    )
