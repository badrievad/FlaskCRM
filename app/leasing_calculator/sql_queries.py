from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from .models import (
    Seller,
    LeasCalculator,
    CommercialOffer,
    ScheduleAnnuity,
    MainAnnuity,
    ScheduleDifferentiated,
    MainDifferentiated,
    ScheduleRegression,
    MainRegression,
)
from .other_utils import dadata_info_company, dadata_result
from .. import db
from logger import logging
from ..deal.models import Bank


def create_or_update_seller_and_link_to_leas_calc(
    new_name,
    new_inn,
    new_address,
    new_phone,
    new_email,
    new_signer,
    calc_id,
    new_based_on,
    new_bank,
    new_current,
):
    """Creates or updates a seller and links it to a LeasCalculator, including bank information."""
    try:
        # Fetch Dadata information
        dadata_info: dict = dadata_info_company(new_inn)
        ogrn = dadata_result(dadata_info)["ogrn"]
        okato = dadata_result(dadata_info)["okato"]
        kpp = dadata_result(dadata_info)["kpp"]
        reg_date = dadata_result(dadata_info)["reg_date"]

        # Initialize current_account if not provided
        current_account = new_current or ""

        # Check if the seller exists
        seller: Seller = Seller.query.filter_by(inn=new_inn).first()

        if seller:
            # Update seller's fields if they have changed
            updated = False
            if seller.name != new_name:
                seller.name = new_name
                updated = True
            if seller.address != new_address:
                seller.address = new_address
                updated = True
            if seller.phone != new_phone:
                seller.phone = new_phone
                updated = True
            if seller.email != new_email:
                seller.email = new_email
                updated = True
            if seller.signer != new_signer:
                seller.signer = new_signer
                updated = True
            if seller.based_on != new_based_on:
                seller.based_on = new_based_on
                updated = True
            if seller.current_account != current_account:
                seller.current_account = current_account
                updated = True
            if seller.okato != okato:
                seller.okato = okato
                updated = True
            if seller.kpp != kpp:
                seller.kpp = kpp
                updated = True
            if seller.date_of_registration != reg_date:
                seller.date_of_registration = reg_date
                updated = True

            # Process bank information
            if new_bank:
                bank_updated = process_bank_info(seller, new_bank)
                if bank_updated:
                    updated = True

            if updated:
                db.session.commit()
        else:
            # Create new seller
            seller = Seller(
                name=new_name,
                inn=new_inn,
                ogrn=ogrn,
                okato=okato,
                kpp=kpp,
                date_of_registration=reg_date,
                address=new_address,
                phone=new_phone,
                email=new_email,
                signer=new_signer,
                based_on=new_based_on,
                current_account=current_account,
            )
            db.session.add(seller)
            db.session.commit()

            # Process bank information
            if new_bank:
                process_bank_info(seller, new_bank)
                db.session.commit()

        # Link the seller to the LeasCalculator
        leas_calc = LeasCalculator.query.get(calc_id)
        if not leas_calc:
            return {"error": "LeasCalculator not found"}, 404

        leas_calc.seller_id = seller.id
        db.session.commit()

        return {"message": "Seller linked to LeasCalculator successfully"}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error: {e}")
        return {"error": "Database error occurred"}, 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred"}, 500


def process_bank_info(seller: Seller, new_bank: dict) -> bool:
    """
    Updates or creates a bank and associates it with the seller.
    Returns True if the bank was updated or created, False otherwise.
    """
    bank_updated = False
    bank_bic = new_bank.get("bic")

    if bank_bic:
        # Check if the bank exists by BIC
        bank = Bank.query.filter_by(bic=bank_bic).first()
        if bank:
            # Update bank details if they have changed
            bank_fields = ["name", "inn", "kpp", "address", "correspondent_account"]
            for field in bank_fields:
                new_value = new_bank.get(field)
                if new_value is not None and getattr(bank, field) != new_value:
                    setattr(bank, field, new_value)
                    bank_updated = True
        else:
            # Create a new bank
            bank = Bank(
                name=new_bank.get("name"),
                inn=new_bank.get("inn"),
                kpp=new_bank.get("kpp"),
                bic=bank_bic,
                address=new_bank.get("address"),
                correspondent_account=new_bank.get("correspondent_account"),
            )
            db.session.add(bank)
            bank_updated = True

        # Associate the bank with the seller
        if seller.bank != bank:
            seller.bank = bank
            bank_updated = True
    else:
        logging.error("BIC not provided in new_bank data.")
        raise ValueError("Bank BIC is required.")

    return bank_updated


def create_commercial_offer_in_db(leas_calculator_id, type_of_schedule):
    try:
        # Создаем запись коммерческого предложения
        new_offer = CommercialOffer(
            leas_calculator_id=leas_calculator_id, type_of_schedule=type_of_schedule
        )

        # Добавляем новую запись в сессию базы данных
        db.session.add(new_offer)
        db.session.commit()

        # Если всё прошло успешно, возвращаем True
        return (
            True,
            new_offer.id,
        )

    except Exception as e:
        # Если произошла ошибка, откатываем изменения
        db.session.rollback()

        # Логируем ошибку для дальнейшего анализа
        logging.error(f"Ошибка при создании коммерческого предложения: {str(e)}")

        # Возвращаем False в случае ошибки
        return False


def get_list_of_commercial_offers(user_login, offer_id=None) -> list:
    logging.info(f"Оффер ID: {offer_id}")
    # Запрос для получения коммерческих предложений
    if offer_id:
        query = (
            db.session.query(CommercialOffer)
            .join(LeasCalculator)
            .options(
                joinedload(CommercialOffer.leas_calculator).joinedload(
                    LeasCalculator.deal
                )
            )
            .filter(CommercialOffer.id == offer_id)
        )
    else:
        query = (
            db.session.query(CommercialOffer)
            .join(LeasCalculator)
            .options(
                joinedload(CommercialOffer.leas_calculator).joinedload(
                    LeasCalculator.deal
                )
            )
            .filter(LeasCalculator.manager_login == user_login)
        )

    # Выполняем запрос
    commercial_offers = query.all()

    # Создаем пустой список для вывода коммерческих предложений с расчетами
    com_offers_list = []

    # Обрабатываем каждое коммерческое предложение
    for offer in commercial_offers:
        # В зависимости от type_of_schedule подгружаем нужные данные
        if offer.type_of_schedule == "annuity":
            schedule_data = ScheduleAnnuity.query.filter_by(
                calc_id=offer.leas_calculator_id
            ).all()
            main_data = MainAnnuity.query.filter_by(
                calc_id=offer.leas_calculator_id
            ).first()
        elif offer.type_of_schedule == "differentiated":
            schedule_data = ScheduleDifferentiated.query.filter_by(
                calc_id=offer.leas_calculator_id
            ).all()
            main_data = MainDifferentiated.query.filter_by(
                calc_id=offer.leas_calculator_id
            ).first()
        elif offer.type_of_schedule == "regressive":
            schedule_data = ScheduleRegression.query.filter_by(
                calc_id=offer.leas_calculator_id
            ).all()
            main_data = MainRegression.query.filter_by(
                calc_id=offer.leas_calculator_id
            ).first()
        else:
            schedule_data = None
            main_data = None

        # Добавляем информацию в итоговый список
        com_offers_list.append(
            {
                "offer": offer,
                "leas_calculator": offer.leas_calculator,
                "schedule_data": schedule_data,
                "main_data": main_data,
                "deal": offer.leas_calculator.deal,  # Добавляем информацию о сделке
            }
        )

    return com_offers_list


def get_list_of_leas_calculators(user_login, calc_id=None) -> list:
    logging.info(f"LeasCalculator ID: {calc_id}")

    # Запрос для получения лизинговых калькуляторов
    if calc_id:
        query = db.session.query(LeasCalculator).filter(LeasCalculator.id == calc_id)
    else:
        query = db.session.query(LeasCalculator).filter(
            LeasCalculator.manager_login == user_login
        )

    # Выполняем запрос
    leas_calculators = query.all()

    # Создаем пустой список для вывода лизинговых калькуляций с расчетами
    leas_calc_list = []

    # Обрабатываем каждый лизинговый калькулятор
    for calc in leas_calculators:
        # Подгружаем данные для всех типов графиков платежей
        schedule_annuity = ScheduleAnnuity.query.filter_by(calc_id=calc.id).all()
        schedule_differentiated = ScheduleDifferentiated.query.filter_by(
            calc_id=calc.id
        ).all()
        schedule_regression = ScheduleRegression.query.filter_by(calc_id=calc.id).all()

        # Подгружаем основные данные для всех типов
        main_annuity = MainAnnuity.query.filter_by(calc_id=calc.id).first()
        main_differentiated = MainDifferentiated.query.filter_by(
            calc_id=calc.id
        ).first()
        main_regression = MainRegression.query.filter_by(calc_id=calc.id).first()

        # Добавляем информацию в итоговый список
        leas_calc_list.append(
            {
                "leas_calculator": calc,
                "schedule_annuity": schedule_annuity,
                "schedule_differentiated": schedule_differentiated,
                "schedule_regression": schedule_regression,
                "main_annuity": main_annuity,
                "main_differentiated": main_differentiated,
                "main_regression": main_regression,
            }
        )

    return leas_calc_list
