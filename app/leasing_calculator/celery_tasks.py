import datetime
import time
import openpyxl

from datetime import date
from logger import logging
from celery import shared_task

from .api_pdf_generate import PDFGeneratorClient
from ..config import CALCULATION_TEMPLATE_PATH, LEAS_CALC_TEMPLATE_PATH
from .models import LeasCalculator, Tranches
from .other_utils import validate_item_price
from .. import db
from ..deal.work_with_folders import CompanyFolderAPI


def intensive_task_simulation(data: dict) -> dict:
    import random
    import string

    user_login = data["login"]  # текущий пользователь

    # Заполняем файл случайными данными
    #  TODO: вот тут нужно все делать

    # Имитация заполнения шаблона
    wb = openpyxl.load_workbook(LEAS_CALC_TEMPLATE_PATH / "ШАБЛОН РАСЧЕТА.xlsx")
    ws = wb.active

    num_rows = 50000
    for _ in range(num_rows):
        row = ["".join(random.choice(string.ascii_letters) for _ in range(10))]
        ws.append(row)

    # КОНЕЦ

    logging.info(data)
    # Записываем в базу данных
    try:
        new_tranche = Tranches(
            tranche_1_size=data["tranches"]["tranche1"]["size"],
            tranche_1_rate=data["tranches"]["tranche1"]["rate"],
            tranche_1_fee=data["tranches"]["tranche1"]["fee"],
            tranche_1_own_fee=data["tranches"]["tranche1"]["own_fee"],
            tranche_1_credit_date=data["tranches"]["tranche1"]["credit_date"],
            tranche_1_payment_date=data["tranches"]["tranche1"]["payment_date"],
            tranche_2_size=data["tranches"]["tranche2"]["size"],
            tranche_2_rate=data["tranches"]["tranche2"]["rate"],
            tranche_2_fee=data["tranches"]["tranche2"]["fee"],
            tranche_2_own_fee=data["tranches"]["tranche2"]["own_fee"],
            tranche_2_credit_date=data["tranches"]["tranche2"]["credit_date"],
            tranche_2_payment_date=data["tranches"]["tranche2"]["payment_date"],
            tranche_3_size=data["tranches"]["tranche3"]["size"],
            tranche_3_rate=data["tranches"]["tranche3"]["rate"],
            tranche_3_fee=data["tranches"]["tranche3"]["fee"],
            tranche_3_own_fee=data["tranches"]["tranche3"]["own_fee"],
            tranche_3_credit_date=data["tranches"]["tranche3"]["credit_date"],
            tranche_3_payment_date=data["tranches"]["tranche3"]["payment_date"],
            tranche_4_size=data["tranches"]["tranche4"]["size"],
            tranche_4_rate=data["tranches"]["tranche4"]["rate"],
            tranche_4_fee=data["tranches"]["tranche4"]["fee"],
            tranche_4_own_fee=data["tranches"]["tranche4"]["own_fee"],
            tranche_4_credit_date=data["tranches"]["tranche4"]["credit_date"],
            tranche_4_payment_date=data["tranches"]["tranche4"]["payment_date"],
            tranche_5_size=data["tranches"]["tranche5"]["size"],
            tranche_5_rate=data["tranches"]["tranche5"]["rate"],
            tranche_5_fee=data["tranches"]["tranche5"]["fee"],
            tranche_5_own_fee=data["tranches"]["tranche5"]["own_fee"],
            tranche_5_credit_date=data["tranches"]["tranche5"]["credit_date"],
            tranche_5_payment_date=data["tranches"]["tranche5"]["payment_date"],
        )
        initial_percent = round((data["initial_payment"] / data["item_price"]) * 100, 2)
        credit_percent = round((data["credit_sum"] / data["item_price"]) * 100, 2)

        new_calc = LeasCalculator(
            item_type=data["item_type"],
            item_year=data["item_year"],
            item_condition=data["item_condition"],
            item_price=data["item_price"],
            item_price_str=validate_item_price(str(data["item_price"])),
            item_name=data["item_name"],
            currency=data["currency"],
            foreign_price=data["foreign_price"],
            foreign_price_str=validate_item_price(str(data["foreign_price"])),
            initial_payment=data["initial_payment"],
            initial_payment_str=validate_item_price(str(data["initial_payment"])),
            initial_payment_percent=initial_percent,
            credit_sum=data["credit_sum"],
            credit_sum_str=validate_item_price(str(data["credit_sum"])),
            credit_sum_percent=credit_percent,
            credit_term=data["credit_term"],
            bank_commission=data["bank_commission"],
            lkmb_commission=data["lkmb_commission"],
            insurance_casko=data["insurance_casko"],
            insurance_osago=data["insurance_osago"],
            health_insurance=data["health_insurance"],
            health_insurance_str=validate_item_price(str(data["health_insurance"])),
            other_insurance=data["other_insurance"],
            other_insurance_str=validate_item_price(str(data["other_insurance"])),
            agent_commission=data["agent_commission"],
            manager_bonus=data["manager_bonus"],
            tracker=data["tracker"],
            tracker_str=validate_item_price(str(data["tracker"])),
            mayak=data["mayak"],
            mayak_str=validate_item_price(str(data["mayak"])),
            fedresurs=data["fedresurs"],
            fedresurs_str=validate_item_price(str(data["fedresurs"])),
            gsm=data["gsm"],
            gsm_str=validate_item_price(str(data["gsm"])),
            mail=data["mail"],
            mail_str=validate_item_price(str(data["mail"])),
            input_period=data["input_period"],
            tranche=new_tranche,
            manager_login=data["login"],
            date=datetime.datetime.now(),
            date_ru=date.today().strftime("%d.%m.%Y"),
        )
        db.session.add(new_calc)
        db.session.commit()

        new_deal_id = new_calc.id

        new_title = f"Лизинговый калькулятор (id_{new_deal_id}).xlsx"
        path_to_xlsx = CALCULATION_TEMPLATE_PATH / new_title

        # Создание директории, если она не существует
        CALCULATION_TEMPLATE_PATH.mkdir(parents=True, exist_ok=True)

        wb.save(path_to_xlsx)

        new_calc.title = new_title
        folder_api = CompanyFolderAPI()
        pdf_api = PDFGeneratorClient(new_deal_id, data["login"])
        pdf_api.generate_pdf()
        new_calc.path_to_file = folder_api.create_commercial_offer(
            path_to_xlsx, user_login
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    result = new_calc.to_dict()

    return result


@shared_task(ignore_result=False)
def long_task(data: dict) -> dict:
    start_time = time.perf_counter()
    result = intensive_task_simulation(data)
    logging.info(f"Время выполнения функции: {time.perf_counter() - start_time}")
    return result
