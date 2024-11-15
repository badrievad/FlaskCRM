from logger import logging

from .. import db
from .deals_validate import DealsValidate
from .models import Client, Deal


def write_deal_to_db(
    title,
    name_without_special_symbols,
    company_inn,
    created_by,
    created_at,
    client_id,
    user_id,
) -> dict:
    """Запись сделки в базу данных"""
    sequence_number, year, dl_number, dl_number_windows = Deal.generate_dl_number()
    new_deal: Deal = Deal(
        title=title,
        company_inn=company_inn,
        name_without_special_symbols=name_without_special_symbols,
        created_by=created_by,
        user_id=user_id,
        created_at=created_at,
        status="active",
        dl_number=dl_number,
        dl_number_windows=dl_number_windows,
        sequence_number=sequence_number,
        year=year,
        client_id=client_id,  # Присваиваем client_id
    )
    db.session.add(new_deal)
    db.session.commit()

    new_deal_with_user = new_deal.user.url_photo

    return new_deal.to_json() | {"created_by_icon": new_deal_with_user}


def write_deal_path_to_db(folder_path: str, deal_id: str) -> None:
    """Write deal path to database"""

    try:
        deal: Deal = Deal.query.get(deal_id)
        deal.deal_path = folder_path
        db.session.commit()
    except Exception as e:
        logging.error(f"Database error: {deal_id}: {e}")


def get_or_create_client(client_data: DealsValidate):
    """
    Получает информацию о клиенте из client_data.
    Если клиент с таким ИНН существует, обновляет его данные при необходимости и возвращает его id.
    Иначе создаёт нового клиента и возвращает его id.
    """
    inn = client_data.get_company_inn
    if not inn:
        raise ValueError("ИНН клиента не указан")

    # Проверяем, существует ли клиент с таким ИНН
    client = Client.query.filter_by(inn=inn).first()
    if client:
        updated = False  # Флаг для отслеживания обновлений

        # Сопоставляем и обновляем поля
        fields_to_update = {
            "name": client_data.get_company_name,
            "ogrn": client_data.get_company_ogrn,
            "kpp": client_data.get_company_kpp,
            "okato": client_data.get_company_okato,
            "address": client_data.get_company_address,
            "signer": client_data.get_company_signer,
            "based_on": client_data.get_company_based_on,
            "date_of_registration": client_data.get_company_reg_date,
            "director": client_data.get_company_signer,
        }

        for field, new_value in fields_to_update.items():
            current_value = getattr(client, field)
            if current_value != new_value:
                setattr(client, field, new_value)
                updated = True

        # Если были изменения, сохраняем их в базе данных
        if updated:
            db.session.commit()

        return client.id
    else:
        # Создаем нового клиента
        new_client = Client(
            name=client_data.get_company_name,
            inn=inn,
            ogrn=client_data.get_company_ogrn,
            kpp=client_data.get_company_kpp,
            okato=client_data.get_company_okato,
            address=client_data.get_company_address,
            signer=client_data.get_company_signer,
            based_on=client_data.get_company_based_on,
            date_of_registration=client_data.get_company_reg_date,
            phone="",
            email="",
            current_account="",
            director=client_data.get_company_signer,
        )
        db.session.add(new_client)
        db.session.commit()
        return new_client.id
