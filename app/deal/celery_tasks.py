import time

from celery import shared_task
from logger import logging
from openpyxl import Workbook


def intensive_task_simulation():
    """Intensive task simulation"""
    import random
    import string

    wb = Workbook()
    ws = wb.active

    num_rows = 1000000
    for _ in range(num_rows):
        row = ["".join(random.choice(string.ascii_letters) for _ in range(10))]
        ws.append(row)

    file_path = "task_result.xlsx"
    wb.save(file_path)

    return file_path


@shared_task(ignore_result=False)
def long_task():
    start_time = time.perf_counter()
    result = intensive_task_simulation()
    logging.info(f"Время выполнения функции: {time.perf_counter() - start_time}")
    return result
