import glob
import os
import shutil
from logger import logging

BASE_PATH: str = "/mnt/c/Users/badrievad/Desktop/Deals"  # test path


def get_id_pattern(company_id: str) -> str:
    return os.path.join(BASE_PATH, f"*(id_{company_id})*")


def create_company_folder(company_name: str, company_id: str) -> None:
    """Создает папку для сделки с id_{company_id}"""

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
    """Удаляет папку сделки с id_{company_id}"""

    pattern: str = get_id_pattern(company_id)
    found: bool = False
    for folder_path in glob.glob(pattern, recursive=True):
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            logging.info(f"Папка {folder_path} успешно удалена.")
            found: bool = True
            break

    if not found:
        logging.info(f"Папка с id_{company_id} не найдена.")


def update_to_archive_company_folder(company_id: str) -> None:
    """Добавляет в название папки тег (Архив)"""

    pattern: str = get_id_pattern(company_id)
    found: bool = False
    for folder_path in glob.glob(pattern, recursive=True):
        if os.path.isdir(folder_path):
            folder_name = os.path.basename(folder_path)  # Текущее имя папки
            parent_dir = os.path.dirname(folder_path)  # Родительская директория
            new_folder_name = f"(Архив) {folder_name}"  # Новое имя папки
            new_folder_path = os.path.join(parent_dir, new_folder_name)
            os.rename(folder_path, new_folder_path)  # Переименовать папку
            logging.info(f"Папка {folder_path} успешно обновлена до {new_folder_path}.")
            found = True
            break

    if not found:
        logging.info(f"Папка с id_{company_id} не найдена.")


def update_to_active_company_folder(company_id: str) -> None:
    """Удаляет из названия папки тег (Архив)"""

    pattern: str = get_id_pattern(company_id)
    found: bool = False
    for folder_path in glob.glob(pattern, recursive=True):
        if os.path.isdir(folder_path):
            folder_name = os.path.basename(folder_path)  # Текущее имя папки
            parent_dir = os.path.dirname(folder_path)  # Родительская директория
            new_folder_name = f"{folder_name}".replace(
                "(Архив) ", ""
            )  # Новое имя папки
            new_folder_path = os.path.join(parent_dir, new_folder_name)
            os.rename(folder_path, new_folder_path)  # Переименовать папку
            logging.info(f"Папка {folder_path} успешно обновлена до {new_folder_path}.")
            found = True
            break

    if not found:
        logging.info(f"Папка с id_{company_id} не найдена.")
