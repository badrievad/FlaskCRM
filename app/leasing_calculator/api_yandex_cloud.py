import boto3
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
    PartialCredentialsError,
)

from logger import logging

from ..config import BUCKET_NAME, CALCULATION_TEMPLATE_PATH


def yandex_download_file_s3(file_name: str) -> str | None:
    """
    Скачивание файла с Yandex Cloud
    """
    try:
        # Создаем сессию и клиент для работы с Yandex Object Storage
        session = boto3.session.Session()
        s3 = session.client(
            service_name="s3", endpoint_url="https://storage.yandexcloud.net"
        )

        download_path = (
            CALCULATION_TEMPLATE_PATH.resolve() / file_name
        )  # Локальный путь, куда будет сохранен файл

        # Загрузка файла
        s3.download_file(BUCKET_NAME, file_name, download_path)
        logging.info(
            f"File '{file_name}' successfully downloaded to '{download_path}'."
        )

        return download_path

    except NoCredentialsError:
        logging.error(
            "No credentials provided. Please check your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )
    except PartialCredentialsError:
        logging.error(
            "Incomplete credentials provided. Please ensure both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set."
        )
    except ClientError as e:
        logging.error(f"Client error occurred: {e}")
        if e.response["Error"]["Code"] == "NoSuchKey":
            logging.error(
                f"The file '{file_name}' does not exist in the bucket '{BUCKET_NAME}'."
            )
    except BotoCoreError as e:
        logging.error(f"An error occurred in Boto3: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def yandex_delete_file_s3(file_name: str) -> None:
    """
    Удаление файла с Yandex Cloud
    """
    try:
        # Создаем сессию и клиент для работы с Yandex Object Storage
        session = boto3.session.Session()
        s3 = session.client(
            service_name="s3", endpoint_url="https://storage.yandexcloud.net"
        )

        # Удаление файла
        s3.delete_object(Bucket=BUCKET_NAME, Key=file_name)
        logging.info(f"File '{file_name}' successfully deleted from Yandex Cloud.")

    except NoCredentialsError:
        logging.error(
            "No credentials provided. Please check your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )
    except PartialCredentialsError:
        logging.error(
            "Incomplete credentials provided. Please ensure both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set."
        )
    except ClientError as e:
        logging.error(f"Client error occurred: {e}")
        if e.response["Error"]["Code"] == "NoSuchKey":
            logging.error(
                f"The file '{file_name}' does not exist in the bucket '{BUCKET_NAME}'."
            )
    except BotoCoreError as e:
        logging.error(f"An error occurred in Boto3: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def yandex_upload_file_s3(file_obj, file_name) -> None:
    try:
        # Создаем сессию и клиент для работы с Yandex Object Storage
        session = boto3.session.Session()
        s3 = session.client(
            service_name="s3", endpoint_url="https://storage.yandexcloud.net"
        )

        # Загрузка файла из объекта FileStorage
        s3.upload_fileobj(file_obj, BUCKET_NAME, file_name)
        logging.info(f"File '{file_name}' successfully uploaded to Yandex Cloud.")

    except NoCredentialsError:
        logging.error(
            "No credentials provided. Please check your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )
    except PartialCredentialsError:
        logging.error(
            "Incomplete credentials provided. Please ensure both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set."
        )
    except ClientError as e:
        logging.error(f"Client error occurred: {e}")
    except BotoCoreError as e:
        logging.error(f"An error occurred in Boto3: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
