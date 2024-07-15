import time

from celery import shared_task
from logger import logging


def intensive_task_simulation():
    """Intensive task simulation"""
    import random
    import string

    for _ in range(3000000):
        "".join(random.choice(string.ascii_letters) for _ in range(10))

    return "Task complete!"


@shared_task(ignore_result=False)
def long_task():
    start_time = time.perf_counter()
    result = intensive_task_simulation()
    logging.info(f"Время выполнения функции: {time.perf_counter() - start_time}")
    return result
