import time
from pathlib import Path

from celery import shared_task

from ..config import PATH_TO_CALENDAR
from logger import logging
from openpyxl import Workbook
from flask_login import current_user


def intensive_task_simulation(login: str) -> str:
    """Intensive task simulation"""
    import random
    import string

    wb = Workbook()
    ws = wb.active

    num_rows: int = 1000000
    for _ in range(num_rows):
        row = ["".join(random.choice(string.ascii_letters) for _ in range(10))]
        ws.append(row)

    logging.info(f"Path: {PATH_TO_CALENDAR}")
    file_path: Path = PATH_TO_CALENDAR / login

    # Проверка существования папки, если нет - создаем
    if not file_path.exists():
        file_path.mkdir(parents=True)

    final_path: str = str(file_path / "calendar.xlsx")

    wb.save(str(final_path))

    return final_path


@shared_task(ignore_result=False)
def long_task(login) -> str:
    start_time = time.perf_counter()
    result = intensive_task_simulation(login)
    logging.info(f"Время выполнения функции: {time.perf_counter() - start_time}")
    return result
