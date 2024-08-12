from .models import Deal
from .. import db
from logger import logging


def write_deal_to_db(
    title, name_without_special_symbols, company_inn, created_by, created_at
) -> dict:
    """Write deal to database"""
    dl_number, dl_number_windows = Deal.generate_dl_number()
    new_deal: Deal = Deal(
        title=title,
        company_inn=company_inn,
        name_without_special_symbols=name_without_special_symbols,
        created_by=created_by,
        created_at=created_at,
        status="active",
        dl_number=dl_number,
        dl_number_windows=dl_number_windows,
    )
    db.session.add(new_deal)
    db.session.commit()

    return new_deal.to_json()


def write_deal_path_to_db(folder_path: str, deal_id: str) -> None:
    """Write deal path to database"""

    try:
        deal: Deal = Deal.query.get(deal_id)
        deal.deal_path = folder_path
        db.session.commit()
    except Exception as e:
        logging.error(f"Database error: {deal_id}: {e}")
