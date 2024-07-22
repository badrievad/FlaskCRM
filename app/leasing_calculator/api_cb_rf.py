import datetime
import requests

from bs4 import BeautifulSoup
from logger import logging


class Bs4Stub:
    """Класс заглушка для метода find"""

    @staticmethod
    def find(*args, **kwargs): ...

    @staticmethod
    def find_all(*args, **kwargs):
        return datetime.date.today().strftime("%d.%m.%Y"), "-"


class CentralBankExchangeRates:

    def __init__(self):
        self._URL = "https://www.cbr.ru/scripts/XML_daily.asp?date_req="  # URL ЦБ РФ
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


class CentralBankKeyRate:

    def __init__(self):
        self._URL: str = "https://www.cbr.ru/hd_base/keyrate/"
        self._soup: BeautifulSoup | Bs4Stub = self._connect()

    def _connect(self) -> BeautifulSoup | Bs4Stub:
        response = requests.get(self._URL)
        if response.status_code == 200:
            _xml_data = response.content
            soup = BeautifulSoup(_xml_data, "xml")
            return soup
        else:
            logging.error(f"Error: {response.status_code}")
            return Bs4Stub()  # заглушка

    def get_key_rate(self) -> dict:
        try:
            table = (
                self._soup.find("div", class_="table-wrapper")
                .find("div", class_="table")
                .find_all("tr")
            )[1]

        except Exception as e:
            logging.error(f"Error: {e}")
            table = Bs4Stub()

        try:
            date, key_rate = map(lambda x: x.text, table.find_all("td"))  # noqa C417
        except Exception as e:
            logging.error(f"Error: {e}")
            date, key_rate = datetime.date.today().strftime("%d.%m.%Y"), "-"

        return {
            "date": date,
            "key_rate": key_rate,
        }
