from .models import Deal
from .. import db


def write_deal_to_db(title, company_inn, created_by, created_at) -> dict:
    """Write deal to database"""
    new_deal: Deal = Deal(
        title=title,
        company_inn=company_inn,
        created_by=created_by,
        created_at=created_at,
        status="active",
    )
    db.session.add(new_deal)
    db.session.commit()

    return new_deal.to_json()
