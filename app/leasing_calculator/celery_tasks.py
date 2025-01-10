import datetime
import time
from datetime import date

from celery import shared_task

from log_conf import logger

from .. import db
from .api_for_leas_calc import post_request_leas_calc, upload_main_info, upload_schedule
from .models import Insurances, LeasCalculator, Tranches
from .other_utils import validate_item_price


def intensive_task_simulation(data: dict) -> dict:
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
            agreement_term=data["agreement_term"],
            reduce_percent=data["reduce_percent"],
            leas_day=data["leas_day"],
            service_life=data["service_life"],
            amortization=data["amortization"],
            nds_size=data["nds_size"],
            differential_payment_increase_factor=data[
                "differential_payment_increase_factor"
            ],
            months_regressive_payments=data["months_regressive_payments"],
            bank_commission=data["bank_commission"],
            lkmb_commission=data["lkmb_commission"],
            agent_commission=data["agent_commission"],
            manager_bonus=data["manager_bonus"],
            tracker=data["tracker"],
            mayak=data["mayak"],
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

        calculation_results = post_request_leas_calc(data, new_calc.id)

        if calculation_results.get("error"):
            logger.error(calculation_results.get("error"))
            raise Exception

        upload_schedule(calculation_results)
        upload_main_info(calculation_results)
        com_off_name = f"Лизинговый калькулятор version 1.9_{new_calc.id}.xlsm"

        new_calc.path_to_xlsx = com_off_name
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    result: dict = {**new_calc.to_dict(), "calc_id": new_calc.id}

    return result


@shared_task(ignore_result=False)
def long_task(data: dict) -> dict:
    start_time = time.perf_counter()
    result = intensive_task_simulation(data)
    logger.info(f"Время выполнения функции: {time.perf_counter() - start_time}")
    return result
