import logging
import logging.handlers

from app.config import PATH_FOR_LOG

# Создаем именованный логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Общий формат для логов
formatter = logging.Formatter(
    "%(asctime)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(levelname)s - %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
)

# 1. Ротация по размеру (например, 5 МБ, храним до 5 бэкапов)
file_handler = logging.handlers.RotatingFileHandler(
    PATH_FOR_LOG, maxBytes=5_000_000, backupCount=5, encoding="utf-8"  # 5 MB
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# 2. Вывод в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# Добавляем оба хендлера к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)
