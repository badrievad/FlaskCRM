import datetime
import time
import openpyxl

from datetime import date
from logger import logging
from celery import shared_task

from .api_pdf_generate import PDFGeneratorClient
from ..config import CALCULATION_TEMPLATE_PATH, LEAS_CALC_TEMPLATE_PATH
from .models import LeasCalculator, Tranches, Insurances
from .other_utils import validate_item_price
from .. import db
from ..deal.work_with_folders import CompanyFolderAPI


def intensive_task_simulation(data: dict) -> dict:
    import random
    import string

    user_login = data["user_login"]  # текущий пользователь

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
    # Записываем в базу данных
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
            tranche_2_size=data["tranches"]["tranche2"]["size"],
            tranche_2_rate=data["tranches"]["tranche2"]["rate"],
            tranche_2_fee=data["tranches"]["tranche2"]["fee"],
            tranche_2_own_fee=data["tranches"]["tranche2"]["own_fee"],
            tranche_2_credit_date=data["tranches"]["tranche2"]["credit_date"],
            tranche_3_size=data["tranches"]["tranche3"]["size"],
            tranche_3_rate=data["tranches"]["tranche3"]["rate"],
            tranche_3_fee=data["tranches"]["tranche3"]["fee"],
            tranche_3_own_fee=data["tranches"]["tranche3"]["own_fee"],
            tranche_3_credit_date=data["tranches"]["tranche3"]["credit_date"],
            tranche_4_size=data["tranches"]["tranche4"]["size"],
            tranche_4_rate=data["tranches"]["tranche4"]["rate"],
            tranche_4_fee=data["tranches"]["tranche4"]["fee"],
            tranche_4_own_fee=data["tranches"]["tranche4"]["own_fee"],
            tranche_4_credit_date=data["tranches"]["tranche4"]["credit_date"],
            tranche_5_size=data["tranches"]["tranche5"]["size"],
            tranche_5_rate=data["tranches"]["tranche5"]["rate"],
            tranche_5_fee=data["tranches"]["tranche5"]["fee"],
            tranche_5_own_fee=data["tranches"]["tranche5"]["own_fee"],
            tranche_5_credit_date=data["tranches"]["tranche5"]["credit_date"],
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
            first_payment_date=data["first_payment_date"],
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
            depr_transport=data["depr_transport"],
            depr_transport_str=validate_item_price(str(data["depr_transport"])),
            travel=data["travel"],
            travel_str=validate_item_price(str(data["travel"])),
            stationery=data["stationery"],
            stationery_str=validate_item_price(str(data["stationery"])),
            internet=data["internet"],
            internet_str=validate_item_price(str(data["internet"])),
            pledge=data["pledge"],
            pledge_str=validate_item_price(str(data["pledge"])),
            bank_pledge=data["bank_pledge"],
            bank_pledge_str=validate_item_price(str(data["bank_pledge"])),
            express=data["express"],
            express_str=validate_item_price(str(data["express"])),
            egrn=data["egrn"],
            egrn_str=validate_item_price(str(data["egrn"])),
            egrul=data["egrul"],
            egrul_str=validate_item_price(str(data["egrul"])),
            input_period=data["input_period"],
            insurance=new_insurance,
            tranche=new_tranche,
            manager_login=data["user_login"],
            date=datetime.datetime.now(),
            date_ru=date.today().strftime("%d.%m.%Y"),
            allocate_vat=data["allocate_vat"],
            allocate_deposit=data["allocate_deposit"],
            allocate_redemption=data["allocate_redemption"],
        )
        db.session.add(new_calc)
        db.session.commit()

        new_deal_id = new_calc.id

        new_title_xlsx = f"Лизинговый калькулятор (id_{new_deal_id}).xlsx"
        path_to_xlsx = CALCULATION_TEMPLATE_PATH / new_title_xlsx

        # Создание директории, если она не существует
        CALCULATION_TEMPLATE_PATH.mkdir(parents=True, exist_ok=True)

        wb.save(path_to_xlsx)

        folder_api = CompanyFolderAPI()
        user_info = {
            "user_login": user_login,
            "user_name": data["user_name"],
            "user_email": data["user_email"],
            "user_phone": data["user_phone"],
        }
        pdf_api = PDFGeneratorClient(new_deal_id, user_info)
        try:
            new_calc.path_to_pdf = pdf_api.generate_pdf()
            new_title_pdf = f"Коммерческое предложение (id_{new_deal_id}).pdf"
            new_calc.title = new_title_pdf
        except Exception as e:
            new_calc.path_to_pdf = None
            logging.error(f"Error generating PDF: {e}")
            logging.info("PDF не создался. Сервис недоступен.")
        new_calc.path_to_xlsx = folder_api.create_commercial_offer(
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
