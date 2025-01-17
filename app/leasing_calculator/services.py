from sqlalchemy.orm import joinedload

from log_conf import logger

from .. import db
from ..deal.models import Deal
from ..deal.work_with_folders import CompanyFolderAPI
from ..leasing_calculator.models import LeasCalculator


def update_calculation_service(calc_id, data):
    try:
        calc = (
            LeasCalculator.query.options(joinedload(LeasCalculator.deal))
            .filter_by(id=calc_id)
            .first()
        )
        if calc is None:
            return {
                "success": False,
                "message": "Calculation not found",
                "status_code": 404,
            }

        deal = calc.deal
        logger.info(f"Found deal: {deal}")
        deal_id = data.get("deal_id")

        updated_data = {
            "id": calc.id,
            "item_name": calc.item_name,
            "item_price": calc.item_price_str,
            "item_type": calc.item_type,
            "date_ru": calc.date_ru,
            "title": deal.title if deal else "",
        }

        if deal_id in [None, "", "-"]:
            logger.info(
                f"Deal_id: {deal_id}. Detaching offer from deal or deal not selected"
            )
        else:
            deals_count = Deal.query.filter_by(id=deal_id).count()
            logger.info(f"Number of deals in DB with id {deal_id}: {deals_count}")

            offers_count = LeasCalculator.query.filter_by(deal_id=deal_id).count()
            logger.info(f"Number of linked calculators: {offers_count}")

            if offers_count >= deals_count:
                if deal is None:
                    return {
                        "success": False,
                        "message": f"Невозможно привязать КП к сделке. Уже привязано: {offers_count}. "
                        f"Можно привязать до: {deals_count}. Сначала необходимо отвязать КП от сделки",
                        "status_code": 400,
                    }
                if int(deal.id) == int(deal_id):
                    logger.info(f"Deal {deal.id} is already linked to calculator")
                    for key, value in data.items():
                        setattr(calc, key, None if value in ["-", "", None] else value)

                    db.session.commit()

                    return {
                        "success": True,
                        "message": "Изменения успешно сохранены",
                        "data": updated_data,
                        "status_code": 200,
                    }
                else:

                    return {
                        "success": False,
                        "message": f"Невозможно привязать КП к сделке. Уже привязано: {offers_count}. "
                        f"Можно привязать до: {deals_count}",
                        "status_code": 400,
                    }

        for key, value in data.items():
            setattr(calc, key, None if value in ["-", "", None] else value)

        db.session.commit()

        path_to_xlsx = calc.path_to_xlsx
        path_to_pdf = calc.path_to_pdf

        folder_api = CompanyFolderAPI()
        logger.info(f"Path: {path_to_xlsx} and deal_id: {deal_id}")

        #  Сохраняем КП и расчет в папке сделки
        folder_api.copy_commercial_offer_to_deal(deal_id, path_to_xlsx, path_to_pdf)

        return {
            "success": True,
            "message": "Изменения успешно сохранены",
            "data": updated_data,
            "status_code": 200,
        }

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating calculator: {str(e)}")
        return {
            "success": False,
            "message": "An error occurred while updating the calculation",
            "error": str(e),
            "status_code": 500,
        }
