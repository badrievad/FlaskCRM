from .models import Deal
from .. import db


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
