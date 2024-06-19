import glob
import os
import shutil
from logger import logging

BASE_PATH: str = "/mnt/c/Users/badrievad/Desktop/Deals"  # test path


def create_company_folder(company_name: str, company_id: str) -> None:
    # Создание основной директории
    main_dir: str = os.path.join(BASE_PATH, f"{company_name} (id_{company_id})")
    os.makedirs(main_dir, exist_ok=True)

    # Список поддиректорий, которые будут созданы внутри основной директории
    subdirectories: list = [
        "БКИ",
        "Договоры",
        "Документы клиента",
        "Документы продавца",
        "Заключение",
        "Расчет",
    ]

    for subdirectory in subdirectories:
        os.makedirs(os.path.join(main_dir, subdirectory), exist_ok=True)


def delete_company_folder(company_id: str) -> None:
    # Шаблон для поиска папки по идентификатору компании
    pattern: str = os.path.join(BASE_PATH, f"*(id_{company_id})*")

    found: bool = False
    for folder_path in glob.glob(pattern, recursive=True):
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            logging.info(f"Папка {folder_path} успешно удалена.")
            found: bool = True
            break

    if not found:
        logging.info(f"Папка с id_{company_id} не найдена.")
