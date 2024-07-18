import datetime
import time

from datetime import date
from logger import logging
from openpyxl import Workbook
from celery import shared_task

from ..config import PATH_TO_CALENDAR
from .models import LeasCalculator
from .other_utils import validate_item_price
from .. import db


def intensive_task_simulation(data: dict) -> dict:
    import random
    import string

    """Intensive task simulation"""

    # Создаем директорию пользователя, если она не существует
    user_dir = PATH_TO_CALENDAR / data["login"]
    if not user_dir.exists():
        user_dir.mkdir(parents=True, exist_ok=True)

    # Создаем новый Excel файл
    wb = Workbook()
    ws = wb.active

    # Заполняем файл случайными данными
    num_rows = 1000000
    for _ in range(num_rows):
        row = ["".join(random.choice(string.ascii_letters) for _ in range(10))]
        ws.append(row)

    # Записываем в базу данных
    try:
        new_calc = LeasCalculator(
            manager_login=data["login"],
            date=datetime.datetime.now(),
            date_ru=date.today().strftime("%d.%m.%Y"),
            item_type=data["item_type"],
            item_price=data["item_price"],
            item_price_str=validate_item_price(data["item_price"]),
            item_name=data["item_name"],
            term=data["term"],
            prepaid_expense=data["prepaid_expense"],
            interest_rate=data["interest_rate"],
        )
        db.session.add(new_calc)
        db.session.commit()

        new_title = f"Лизинговый калькулятор (id_{new_calc.id}).xlsx"
        new_calc.title = new_title
        new_calc.path_to_file = str(user_dir)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    # Инициализируем путь к файлу
    file_path = user_dir / new_title

    # Сохраняем файл
    try:
        wb.save(str(file_path))
    except Exception as e:
        # Если не удалось сохранить файл, откатываем транзакцию
        db.session.delete(new_calc)
        db.session.commit()
        raise e

    result = {
        "title": new_title,
        "date_ru": new_calc.date_ru,
        "manager_login": new_calc.manager_login,
        "item_type": new_calc.item_type,
        "item_name": new_calc.item_name,
        "item_price": new_calc.item_price,
        "item_price_str": new_calc.item_price_str,
        "term": new_calc.term,
        "prepaid_expense": new_calc.prepaid_expense,
        "interest_rate": new_calc.interest_rate,
    }

    return result


@shared_task(ignore_result=False)
def long_task(data: dict) -> dict:
    start_time = time.perf_counter()
    result = intensive_task_simulation(data)
    logging.info(f"Время выполнения функции: {time.perf_counter() - start_time}")
    return result
