import requests

from log_conf import logger

from ..config import URL_PDF_API


class PDFGeneratorClient:
    def __init__(self, deal_id, user_info: dict, base_url=URL_PDF_API):
        self.base_url = base_url
        self.deal_id = deal_id
        self.user_info = user_info

    def generate_pdf(self):
        """Отправляет запрос на генерацию PDF и возвращает путь к файлу."""
        url = f"{self.base_url}/generate_pdf"
        payload = {
            "calc_id": self.deal_id,
            **self.user_info,
        }

        logger.info(f"Sending POST request to {url} with payload: {payload}")

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "Completed":
                logger.info(f"PDF создан: {data['pdf_path']}")
                return data["pdf_path"]
            else:
                logger.info("Процесс генерации PDF не завершен.")
        else:
            logger.info(f"Ошибка при запросе: {response.status_code}")
            response.raise_for_status()

        return None
