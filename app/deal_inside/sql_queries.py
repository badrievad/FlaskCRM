from flask_login import current_user

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
    deal = Deal.query.get(deal_id)
    if not deal:
        return None, "Deal not found"

    deal.created_by = new_created_by

    try:
        db.session.commit()
        return deal, None
    except Exception as e:
        db.session.rollback()  # Откат транзакции в случае ошибки
        return None, str(e)
