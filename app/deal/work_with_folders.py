import requests

from app.config import URL_FOLDER_API
from logger import logging


class CompanyFolderAPI:
    def __init__(self):
        self.base_url = URL_FOLDER_API

    def create_folder(self, company_name: str, company_id: str, dl_number: str):
        """Функция для создания папки сделки"""

        url = f"{self.base_url}/create"
        data = {
            "company_name": company_name,
            "company_id": company_id,
            "dl_number": dl_number,
        }
        logging.info(f"Sending POST request to {url} with data: {data}")
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Проверка на ошибки HTTP
            response_json = response.json()
            return response_json["path_to_folder"]
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise PermissionError from e

    def delete_folder(self, company_id: str):
        url = f"{self.base_url}/delete/{company_id}"
        logging.info(f"Sending DELETE request to {url}")
        try:
            response = requests.delete(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise PermissionError from e

    def active_or_archive_folder(self, company_id: str, dl_number: str, status: str):
        """Функция переименования папки сделки в активные или архивные"""

        urls = {
            "active": f"{self.base_url}/activate/{company_id}",
            "archive": f"{self.base_url}/archive/{company_id}",
        }

        if status not in urls:
            logging.error(f"Invalid status: {status}")
            raise ValueError(f"Invalid status: {status}")

        logging.info(f"Sending PUT request to {urls[status]}")
        data = {
            "dl_number": dl_number,
        }
        try:
            response = requests.put(urls[status], json=data)
            response.raise_for_status()
            response_json = response.json()
            return response_json["path_to_folder"]
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise

    def is_available(self) -> bool:
        url = f"{self.base_url}/is_available"
        logging.info(f"Sending GET request to {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("available", False)
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise PermissionError from e

    def copy_commercial_offer_to_deal(
        self, company_id: str, xlsx_path: str, pdf_path: str
    ):
        """Функция для копирования коммерческого предложения в папку сделки"""

        url = f"{self.base_url}/commercial-offer/upload"
        logging.info(f"Sending POST request to {url} with company_id: {company_id}")

        if company_id in [None, "", "-"]:
            logging.info(
                f"Company_id: {company_id}. Detaching offer from deal or deal not selected"
            )
            return

        try:
            data = {
                "company_id": company_id,
                "xlsx_path": xlsx_path,
                "pdf_path": pdf_path,
            }
            response = requests.post(url, json=data)
            response.raise_for_status()  # Проверка на ошибки HTTP

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to upload file: {e}")
            raise PermissionError from e
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise

    def create_commercial_offer(self, file_path: str, user_login: str):
        """Функция для создания КП на сервере"""

        url = f"{self.base_url}/commercial-offer/create"

        # Открытие файла и подготовка данных для отправки
        with open(file_path, "rb") as file_data:
            files = {"file": file_data}
            data = {"user_login": user_login}

            # Отправка POST-запроса
            response = requests.post(url, files=files, data=data)

            # Проверка статуса ответа и извлечение path_to_xlsx
            if response.status_code == 200:
                response_data = response.json()
                path_to_xlsx = response_data.get("path_to_xlsx")
                logging.info("Success:", path_to_xlsx)
                return path_to_xlsx
            else:
                logging.info("Error:", response.status_code, response.text)
                response.raise_for_status()
