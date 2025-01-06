from flask import jsonify

from . import client_application_bp


@client_application_bp.route("/latest-version", methods=["GET"])
def latest_version():
    """
    Возвращает информацию о последней версии клиентского приложения.
    """
    return jsonify(
        {
            "version": "1.0.1",  # Текущая версия на сервере
            "download_url": "https://storage.yandexcloud.net/commercial-offers1/client-app/client_app_v1.1.0.exe?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=YCAJEvYd17LdIreIRxjtTa3G4%2F20250106%2Fru-central1%2Fs3%2Faws4_request&X-Amz-Date=20250106T133136Z&X-Amz-Expires=2592000&X-Amz-Signature=9E1A2CCA4B041652570ABA7C162E1FBACA337332D2CBAB88EFED8ED768FF5D1D&X-Amz-SignedHeaders=host",  # Ссылка на скачивание
        }
    )
