import time
from datetime import date
from logger import logging
from openpyxl import Workbook
from celery import shared_task

from ..config import PATH_TO_CALENDAR
from .models import LeasCalculator
from .. import db


def intensive_task_simulation(login: str) -> str:
    import random
    import string

    """Intensive task simulation"""

    # Создаем директорию пользователя, если она не существует
    user_dir = PATH_TO_CALENDAR / login
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
        new_calc = LeasCalculator(manager_login=login, date=date.today())
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

    return str(file_path)


@shared_task(ignore_result=False)
def long_task(login) -> str:
    start_time = time.perf_counter()
    result = intensive_task_simulation(login)
    logging.info(f"Время выполнения функции: {time.perf_counter() - start_time}")
    return result
