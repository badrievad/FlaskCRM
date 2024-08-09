import requests

from typing import LiteralString
from app.config import URL_FOLDER_API
from logger import logging


class CompanyFolderAPI:
    def __init__(self):
        self.base_url = URL_FOLDER_API

    def create_folder(self, company_name: str, company_id: str, dl_number: str):
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
            return response.json()
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

    def archive_folder(self, company_id: str, dl_number: str):
        url = f"{self.base_url}/archive/{company_id}"
        logging.info(f"Sending PUT request to {url}")
        data = {
            "dl_number": dl_number,
        }
        try:
            response = requests.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise PermissionError from e

    def activate_folder(self, company_id: str, dl_number: str):
        url = f"{self.base_url}/activate/{company_id}"
        logging.info(f"Sending PUT request to {url}")
        data = {
            "dl_number": dl_number,
        }
        try:
            response = requests.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise PermissionError from e

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

    def send_commercial_offer(
        self, file_path: LiteralString | str | bytes, company_id: str
    ):
        url = f"{self.base_url}/commercial-offer/upload"
        logging.info(
            f"Sending POST request to {url} with file: {file_path} and company_id: {company_id}"
        )

        if company_id in [None, "", "-"]:
            logging.info(
                f"Company_id: {company_id}. Detaching offer from deal or deal not selected"
            )
            return

        try:
            with open(file_path, "rb") as file:
                logging.info(f"File opened: {file_path}")
                files = {"file": file}
                data = {"company_id": company_id}
                logging.info(f"Type file: {type(file)}")
                logging.info(f"Type company_id: {type(company_id)}")
                response = requests.post(url, files=files, data=data)
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
        url = f"{self.base_url}/commercial-offer/create"

        # Открытие файла и подготовка данных для отправки
        with open(file_path, "rb") as file_data:
            files = {"file": file_data}
            data = {"user_login": user_login}

            # Отправка POST-запроса
            response = requests.post(url, files=files, data=data)

            # Проверка статуса ответа и извлечение path_to_file
            if response.status_code == 200:
                response_data = response.json()
                path_to_file = response_data.get("path_to_file")
                logging.info("Success:", path_to_file)
                return path_to_file
            else:
                logging.info("Error:", response.status_code, response.text)
                response.raise_for_status()
