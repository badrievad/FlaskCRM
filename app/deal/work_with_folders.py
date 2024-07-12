import requests
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

    def archive_folder(self, company_id: str):
        url = f"{self.base_url}/archive/{company_id}"
        logging.info(f"Sending PUT request to {url}")
        try:
            response = requests.put(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise PermissionError from e

    def activate_folder(self, company_id: str):
        url = f"{self.base_url}/activate/{company_id}"
        logging.info(f"Sending PUT request to {url}")
        try:
            response = requests.put(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise PermissionError from e
