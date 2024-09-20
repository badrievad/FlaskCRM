from sqlalchemy.exc import SQLAlchemyError

from .. import db
from ..deal.models import Deal, Client
from ..leasing_calculator.models import LeasCalculator
from ..user.models import User
from logger import logging


def get_users_with_roles(roles, current_user_id):
    result = (
        User.query.filter(User.role.in_(roles))
        .filter(User.fullname != current_user_id)
        .all()
    )
    return [{"name": user.fullname, "role": user.role} for user in result]


def update_deal_created_by(deal_id, new_created_by):
    # Найдем основную сделку по её id
    deal = Deal.query.get(deal_id)
    if not deal:
        return None, "Deal not found"

    # Если у сделки есть group_id, обновляем все сделки с этим group_id
    if deal.group_id:
        # Найдем все сделки с тем же group_id
        related_deals = Deal.query.filter_by(group_id=deal.group_id).all()

        if not related_deals:
            return None, "No deals found in the group"

        # Обновляем ответственного для всех сделок в группе
        for related_deal in related_deals:
            related_deal.created_by = new_created_by

        try:
            # Сохраняем изменения в базе данных
            db.session.commit()
            return related_deals, None  # Возвращаем список обновленных сделок
        except Exception as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            return None, str(e)
    else:
        # Если group_id нет, обновляем только текущую сделку
        deal.created_by = new_created_by

        try:
            # Сохраняем изменения в базе данных
            db.session.commit()
            return deal, None  # Возвращаем одну обновленную сделку
        except Exception as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            return None, str(e)


def delete_seller_by_calc_id(calc_id):
    try:
        # Найти КП по calc_id
        calculator = LeasCalculator.query.get(calc_id)

        if not calculator:
            return False, "КП не найдено"

        # Убираем seller_id
        calculator.seller_id = None

        db.session.commit()

        return True, "Поставщик удален"

    except Exception as e:
        db.session.rollback()
        logging.error(f"Ошибка при удалении продавца для calc_id {calc_id}: {str(e)}")
        return False, str(e)


def delete_calculator_section(calc_id, dl_number):
    try:
        # Находим запись LeasCalculator по calc_id
        if calc_id:
            calculator = LeasCalculator.query.get(calc_id)
        else:
            calculator = None

        # Находим сделку, связанную с калькулятором
        deal = Deal.query.filter_by(dl_number=dl_number).first()

        if not deal:
            return False, "Сделка по № ДЛ не найдена"

        # Обнуляем deal_id у калькулятора и group_id у сделки
        if calculator:
            calculator.deal_id = None
        deal.group_id = None

        db.session.commit()

        return True, "Договор успешно отвязан от сделки"

    except Exception as e:
        db.session.rollback()  # Откат транзакции в случае ошибки
        return False, f"Ошибка при отвязке секции: {str(e)}"


def update_client_in_db(
    deal_id,
    new_address,
    new_phone,
    new_email,
    new_signer,
    new_base_on,
    new_bank,
    new_current,
):
    try:
        # Находим сделку по deal_id
        deal = Deal.query.get(deal_id)
        if not deal:
            return {"success": False, "message": "Сделка не найдена"}, 404

        # Получаем client_id из сделки
        client_id = deal.client_id
        if not client_id:
            return {"success": False, "message": "Клиент не связан с этой сделкой"}, 404

        # Находим клиента по client_id
        client = Client.query.get(client_id)
        if not client:
            return {"success": False, "message": "Клиент не найден"}, 404

        # Обновляем поля клиента, если они изменились
        updated = False
        if new_address is not None and client.address != new_address:
            client.address = new_address
            updated = True
        if new_phone is not None and client.phone != new_phone:
            client.phone = new_phone
            updated = True
        if new_email is not None and client.email != new_email:
            client.email = new_email
            updated = True
        if new_signer is not None and client.signer != new_signer:
            client.signer = new_signer
            updated = True
        if new_base_on is not None and client.based_on != new_base_on:
            client.based_on = new_base_on
            updated = True
        if new_current is not None and client.current_account != new_current:
            client.current_account = new_current
            updated = True

        if updated:
            db.session.commit()
            return {"success": True, "message": "Данные клиента успешно обновлены"}, 200
        else:
            return {"success": True, "message": "Нет изменений в данных клиента"}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Ошибка при обновлении данных клиента: {e}")
        return {
            "success": False,
            "message": "Ошибка базы данных при обновлении данных клиента",
        }, 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"Неизвестная ошибка при обновлении данных клиента: {e}")
        return {
            "success": False,
            "message": "Произошла ошибка при обновлении данных клиента",
        }, 500
