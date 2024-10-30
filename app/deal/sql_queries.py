import uuid

from .. import db
from .models import Deal


def merge_deals_in_db(deal_ids):
    """Функция для объединения сделок в базе данных."""
    # Поиск сделок по ID
    deals = Deal.query.filter(Deal.id.in_(deal_ids)).all()

    # Проверка, что все сделки найдены
    if len(deals) != len(deal_ids):
        return None, "Некоторые сделки не найдены"

    # Генерация уникального group_id для объединенных сделок
    group_id = str(uuid.uuid4())

    # Присвоение group_id выбранным сделкам
    for deal in deals:
        deal.group_id = group_id

    # Сохранение изменений в базе данных
    db.session.commit()

    return group_id, None  # Возвращаем group_id и отсутствие ошибок
