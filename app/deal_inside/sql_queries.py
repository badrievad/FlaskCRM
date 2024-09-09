from .. import db
from ..deal.models import Deal
from ..user.models import User


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
