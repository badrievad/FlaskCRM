import re
from datetime import datetime

from dadata import Dadata

from logger import logging

from ..config import suggestions_token


def validate_item_price(price: str) -> str:
    # Проверка на наличие букв в строке
    if re.search(r"[a-zA-Z]", price):
        raise ValueError("Input contains letters, which is not allowed.")

    # Проверка на пустую строку
    if not price:
        return "0,00"

    # Удаляем пробелы из строки
    price: str = price.replace(" ", "")

    # Заменяем точку на запятую, если необходимо
    price: str = price.replace(".", ",")

    # Если нет дробной части, добавляем ",00"
    if "," not in price:
        price += ",00"
    else:
        # Убедимся, что дробная часть существует и состоит из двух цифр
        integer_part, fractional_part = price.split(",")
        if fractional_part == "":
            fractional_part = "00"
        elif len(fractional_part) == 1:
            fractional_part += "0"
        elif len(fractional_part) > 2:
            fractional_part = fractional_part[:2]
        price = integer_part + "," + fractional_part

    # Добавляем пробелы как разделители тысяч
    integer_part, fractional_part = price.split(",")
    integer_part_with_spaces: str = re.sub(r"\B(?=(\d{3})+(?!\d))", " ", integer_part)

    # Формируем окончательный результат
    formatted_price: str = integer_part_with_spaces + "," + fractional_part
    return formatted_price


def dadata_info_company(inn: str) -> dict:
    try:
        dadata = Dadata(suggestions_token)
        result = dadata.find_by_id("party", inn)[0]
    except Exception as e:
        logging.error(f"Error: {e}")
        result = {}

    return result


def dadata_result(dadata_object: dict) -> dict:
    ogrn_date_ms = dadata_object.get("data", {}).get("ogrn_date", "")
    if ogrn_date_ms:
        try:
            ogrn_date_s = int(ogrn_date_ms) / 1000
            reg_date = datetime.fromtimestamp(ogrn_date_s).date()
        except (ValueError, TypeError):
            reg_date = "-"
    else:
        reg_date = "-"
    return {
        "inn": dadata_object.get("data", {}).get("inn", "-"),
        "kpp": dadata_object.get("data", {}).get("kpp", "-"),
        "ogrn": dadata_object.get("data", {}).get("ogrn", "-"),
        "okato": dadata_object.get("data", {}).get("okato", "-"),
        "name": dadata_object.get("value", "-"),
        "reg_date": reg_date,
        "address": dadata_object.get("data", {}).get("address", {}.get("value", "-")),
    }
