import datetime
import requests

from bs4 import BeautifulSoup
from logger import logging


class Bs4Stub:
    """Класс заглушка для метода find"""

    @staticmethod
    def find(*args, **kwargs): ...


class ApiCentralBank:

    _URL = "https://www.cbr.ru/scripts/XML_daily.asp?date_req="  # API ЦБ

    def __init__(self):
        self._soup = self._connect(self._get_date())
        self._prev_soup = self._connect(self._get_previous_date())

    def _connect(self, data: str) -> BeautifulSoup | Bs4Stub:
        response = requests.get(f"{self._URL}{data}")
        if response.status_code == 200:
            _xml_data = response.content
            soup = BeautifulSoup(_xml_data, "xml")
            return soup
        else:
            logging.error(f"Error: {response.status_code}")
            return Bs4Stub()  # заглушка

    @staticmethod
    def _get_date() -> str:
        current_date = datetime.date.today()
        next_day = current_date + datetime.timedelta(days=1)
        return next_day.strftime("%d.%m.%Y")

    def _get_previous_date(self) -> str:
        current_date: str = self._soup.find("ValCurs").get("Date")
        previous_day: datetime = datetime.datetime.strptime(
            current_date, "%d.%m.%Y"
        ) - datetime.timedelta(days=1)
        return previous_day.strftime("%d.%m.%Y")

    def get_exchange_rates(self) -> dict:

        # Находим на какую дату выгружены данные
        date: str = self._soup.find("ValCurs").get("Date")

        return {
            "today": {
                "date": date,
                "usd": self._soup.find("Valute", {"ID": "R01235"}).find("Value").text,
                "eur": self._soup.find("Valute", {"ID": "R01239"}).find("Value").text,
                "cny": self._soup.find("Valute", {"ID": "R01375"}).find("Value").text,
            },
            "previous_day": {
                "date": self._get_previous_date(),
                "usd": self._prev_soup.find("Valute", {"ID": "R01235"})
                .find("Value")
                .text,
                "eur": self._prev_soup.find("Valute", {"ID": "R01239"})
                .find("Value")
                .text,
                "cny": self._prev_soup.find("Valute", {"ID": "R01375"})
                .find("Value")
                .text,
            },
        }
