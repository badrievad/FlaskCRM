# Основной путь для директорий
import os

BASE_PATH: str = "/mnt/c/Users/badrievad/Desktop/Deals"


def create_company_folders(company_name: str, company_id: str) -> None:
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
