from flask import jsonify

from . import client_application_bp


@client_application_bp.route("/latest-version", methods=["GET"])
def latest_version():
    """
    Возвращает информацию о последней версии клиентского приложения.
    """
    return jsonify(
        {
            "version": "1.0.2",  # Текущая версия на сервере
            "download_url": "https://storage.yandexcloud.net/commercial-offers1/client-app/client_app_v1.0.2.exe?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=YCAJEvYd17LdIreIRxjtTa3G4%2F20250107%2Fru-central1%2Fs3%2Faws4_request&X-Amz-Date=20250107T092130Z&X-Amz-Expires=3600&X-Amz-Signature=6B9848F1241687D1E272FE769940C572DDFD10511EC8ED76D98439FB32BB9B02&X-Amz-SignedHeaders=host",  # Ссылка на скачивание
        }
    )
