from datetime import date, datetime

from sqlalchemy import desc  # type: ignore
from sqlalchemy.exc import SQLAlchemyError  # type: ignore
from sqlalchemy.orm import joinedload  # type: ignore

from log_conf import logger

from .. import db
from ..deal.models import Bank
from .api_for_leas_calc import upload_main_info, upload_schedule
from .models import (
    CommercialOffer,
    Insurances,
    LeasCalculator,
    MainAnnuity,
    MainDifferentiated,
    MainRegression,
    ScheduleAnnuity,
    ScheduleDifferentiated,
    ScheduleRegression,
    Seller,
    Tranches,
)
from .other_utils import dadata_info_company, dadata_result, validate_item_price


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
        logger.error(f"Database error: {e}")
        return {"error": "Database error occurred"}, 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"An unexpected error occurred: {e}")
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
        logger.error("BIC not provided in new_bank data.")
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
        logger.error(f"Ошибка при создании коммерческого предложения: {str(e)}")

        # Возвращаем False в случае ошибки
        return False


def get_list_of_commercial_offers(user_login, offer_id=None) -> list:
    logger.info(f"Оффер ID: {offer_id}")
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
            .order_by(desc(CommercialOffer.id))
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
            .order_by(desc(CommercialOffer.id))
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
    logger.info(f"LeasCalculator ID: {calc_id}")

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


def create_new_leas_calc(user_login) -> int | None:
    try:
        new_calc = LeasCalculator(
            manager_login=user_login,
            date=datetime.now(),
            date_ru=date.today().strftime("%d.%m.%Y"),
        )
        db.session.add(new_calc)
        db.session.commit()
        return new_calc.id
    except SQLAlchemyError as e:
        logger.error(f"Error creating new LeasCalculator. Error: {str(e)}")
        return None
    except Exception as e:
        logger.error(str(e))
        return None


def write_information_to_leas_calc(data: dict, calc_id, file_name: str) -> None:
    try:
        new_insurance = Insurances(
            insurance_casko1=data["insurances"]["insurance1"]["casko"],
            insurance_casko2=data["insurances"]["insurance2"]["casko"],
            insurance_casko3=data["insurances"]["insurance3"]["casko"],
            insurance_casko4=data["insurances"]["insurance4"]["casko"],
            insurance_casko5=data["insurances"]["insurance5"]["casko"],
            insurance_osago1=data["insurances"]["insurance1"]["osago"],
            insurance_osago2=data["insurances"]["insurance2"]["osago"],
            insurance_osago3=data["insurances"]["insurance3"]["osago"],
            insurance_osago4=data["insurances"]["insurance4"]["osago"],
            insurance_osago5=data["insurances"]["insurance5"]["osago"],
            health_insurance1=data["insurances"]["insurance1"]["health"],
            health_insurance1_str=validate_item_price(
                str(data["insurances"]["insurance1"]["health"])
            ),
            health_insurance2=data["insurances"]["insurance2"]["health"],
            health_insurance2_str=validate_item_price(
                str(data["insurances"]["insurance2"]["health"])
            ),
            health_insurance3=data["insurances"]["insurance3"]["health"],
            health_insurance3_str=validate_item_price(
                str(data["insurances"]["insurance3"]["health"])
            ),
            health_insurance4=data["insurances"]["insurance4"]["health"],
            health_insurance4_str=validate_item_price(
                str(data["insurances"]["insurance4"]["health"])
            ),
            health_insurance5=data["insurances"]["insurance5"]["health"],
            health_insurance5_str=validate_item_price(
                str(data["insurances"]["insurance5"]["health"])
            ),
            other_insurance1=data["insurances"]["insurance1"]["other"],
            other_insurance1_str=validate_item_price(
                str(data["insurances"]["insurance1"]["other"])
            ),
            other_insurance2=data["insurances"]["insurance2"]["other"],
            other_insurance2_str=validate_item_price(
                str(data["insurances"]["insurance2"]["other"])
            ),
            other_insurance3=data["insurances"]["insurance3"]["other"],
            other_insurance3_str=validate_item_price(
                str(data["insurances"]["insurance3"]["other"])
            ),
            other_insurance4=data["insurances"]["insurance4"]["other"],
            other_insurance4_str=validate_item_price(
                str(data["insurances"]["insurance4"]["other"])
            ),
            other_insurance5=data["insurances"]["insurance5"]["other"],
            other_insurance5_str=validate_item_price(
                str(data["insurances"]["insurance5"]["other"])
            ),
        )
        new_tranche = Tranches(
            tranche_1_size=data["tranches"]["tranche1"]["size"],
            tranche_1_rate=data["tranches"]["tranche1"]["rate"],
            tranche_1_fee=data["tranches"]["tranche1"]["fee"],
            tranche_1_own_fee=data["tranches"]["tranche1"]["own_fee"],
            tranche_1_credit_date=data["tranches"]["tranche1"]["credit_date"],
            tranche_1_payment_deferment=data["tranches"]["tranche1"][
                "payment_deferment"
            ],
            tranche_2_size=data["tranches"]["tranche2"]["size"],
            tranche_2_rate=data["tranches"]["tranche2"]["rate"],
            tranche_2_fee=data["tranches"]["tranche2"]["fee"],
            tranche_2_own_fee=data["tranches"]["tranche2"]["own_fee"],
            tranche_2_credit_date=data["tranches"]["tranche2"]["credit_date"],
            tranche_2_payment_deferment=data["tranches"]["tranche2"][
                "payment_deferment"
            ],
            tranche_3_size=data["tranches"]["tranche3"]["size"],
            tranche_3_rate=data["tranches"]["tranche3"]["rate"],
            tranche_3_fee=data["tranches"]["tranche3"]["fee"],
            tranche_3_own_fee=data["tranches"]["tranche3"]["own_fee"],
            tranche_3_credit_date=data["tranches"]["tranche3"]["credit_date"],
            tranche_3_payment_deferment=data["tranches"]["tranche3"][
                "payment_deferment"
            ],
            tranche_4_size=data["tranches"]["tranche4"]["size"],
            tranche_4_rate=data["tranches"]["tranche4"]["rate"],
            tranche_4_fee=data["tranches"]["tranche4"]["fee"],
            tranche_4_own_fee=data["tranches"]["tranche4"]["own_fee"],
            tranche_4_credit_date=data["tranches"]["tranche4"]["credit_date"],
            tranche_4_payment_deferment=data["tranches"]["tranche4"][
                "payment_deferment"
            ],
            tranche_5_size=data["tranches"]["tranche5"]["size"],
            tranche_5_rate=data["tranches"]["tranche5"]["rate"],
            tranche_5_fee=data["tranches"]["tranche5"]["fee"],
            tranche_5_own_fee=data["tranches"]["tranche5"]["own_fee"],
            tranche_5_credit_date=data["tranches"]["tranche5"]["credit_date"],
            tranche_5_payment_deferment=data["tranches"]["tranche5"][
                "payment_deferment"
            ],
        )
        initial_percent = round((data["initial_payment"] / data["item_price"]) * 100, 2)
        credit_percent = round((data["credit_sum"] / data["item_price"]) * 100, 2)

        calculator = LeasCalculator.query.get(calc_id)
        calculator.item_type = data["item_type"]
        calculator.item_year = data["item_year"]
        calculator.item_condition = data["item_condition"]
        calculator.item_price = data["item_price"]
        calculator.item_price_str = validate_item_price(str(data["item_price"]))
        calculator.item_name = data["item_name"]
        calculator.currency = data["currency"]
        calculator.foreign_price = data["foreign_price"]
        calculator.foreign_price_str = validate_item_price(str(data["foreign_price"]))
        calculator.initial_payment = data["initial_payment"]
        calculator.initial_payment_str = validate_item_price(
            str(data["initial_payment"])
        )
        calculator.initial_payment_percent = initial_percent
        calculator.credit_sum = data["credit_sum"]
        calculator.credit_sum_str = validate_item_price(str(data["credit_sum"]))
        calculator.credit_sum_percent = credit_percent
        calculator.credit_term = data["credit_term"]
        calculator.agreement_term = data["agreement_term"]
        calculator.reduce_percent = data["reduce_percent"]
        calculator.leas_day = data["leas_day"]
        calculator.service_life = data["service_life"]
        calculator.amortization = data["amortization"]
        calculator.nds_size = data["nds_size"]
        calculator.bank_commission = data["bank_commission"]
        calculator.lkmb_commission = data["lkmb_commission"]
        calculator.agent_commission = data["agent_commission"]
        calculator.manager_bonus = data["manager_bonus"]
        calculator.tracker = data["tracker"]
        calculator.mayak = data["mayak"]
        calculator.fedresurs = data["fedresurs"]
        calculator.fedresurs_str = validate_item_price(str(data["fedresurs"]))
        calculator.gsm = data["gsm"]
        calculator.gsm_str = validate_item_price(str(data["gsm"]))
        calculator.mail = data["mail"]
        calculator.mail_str = validate_item_price(str(data["mail"]))
        calculator.depr_transport = data["depr_transport"]
        calculator.depr_transport_str = validate_item_price(str(data["depr_transport"]))
        calculator.travel = data["travel"]
        calculator.travel_str = validate_item_price(str(data["travel"]))
        calculator.stationery = data["stationery"]
        calculator.stationery_str = validate_item_price(str(data["stationery"]))
        calculator.internet = data["internet"]
        calculator.internet_str = validate_item_price(str(data["internet"]))
        calculator.pledge = data["pledge"]
        calculator.pledge_str = validate_item_price(str(data["pledge"]))
        calculator.bank_pledge = data["bank_pledge"]
        calculator.bank_pledge_str = validate_item_price(str(data["bank_pledge"]))
        calculator.express = data["express"]
        calculator.express_str = validate_item_price(str(data["express"]))
        calculator.egrn = data["egrn"]
        calculator.egrn_str = validate_item_price(str(data["egrn"]))
        calculator.egrul = data["egrul"]
        calculator.egrul_str = validate_item_price(str(data["egrul"]))
        calculator.input_period = data["input_period"]
        calculator.insurance = new_insurance
        calculator.tranche = new_tranche
        calculator.allocate_vat = data["allocate_vat"]
        calculator.allocate_deposit = data["allocate_deposit"]
        calculator.allocate_redemption = data["allocate_redemption"]

        db.session.commit()

        upload_schedule(data)
        upload_main_info(data)

        calculator.status = "completed"
        calculator.path_to_xlsx = file_name

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e
