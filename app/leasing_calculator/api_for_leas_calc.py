from datetime import date

import requests
from flask import jsonify
from pydantic import BaseModel, Field, ValidationError, field_validator
from sqlalchemy.exc import SQLAlchemyError

from logger import logging

from .. import db
from ..config import URL_XLSX_API
from .models import (
    MainAnnuity,
    MainDifferentiated,
    MainRegression,
    ScheduleAnnuity,
    ScheduleDifferentiated,
    ScheduleRegression,
)
from .other_utils import validate_item_price


class MainInfoItem(BaseModel):
    calc_id: int
    lease_agreement_amount: float
    vat_refund: float
    save_income_tax: float
    total_cost: float
    redemption_value: float
    transaction_processing_fee: float
    company_margin: float
    effective_rate: float
    increase_rate: float


class ScheduleItem(BaseModel):
    calc_id: int = Field(..., gt=0, description="Identifier for the calculation")
    payment_date: date = Field(
        ..., description="Date of the payment in YYYY-MM-DD format"
    )
    leas_payment_amount: float = Field(..., ge=0, description="Amount of lease payment")
    early_repayment_amount: float = Field(
        ..., ge=0, description="Amount of early repayment"
    )

    @field_validator("payment_date")
    def validate_payment_date(cls, value):  # noqa
        if value < date.today():
            raise ValueError("payment_date cannot be in the past")
        return value


def upload_schedule(data: dict):
    """
    Записывает в БД графики из расчетов Димы.
    """
    logging.info("Received data for schedule upload.")
    schedule_models = {
        "annuity": ScheduleAnnuity,
        "differentiated": ScheduleDifferentiated,
        "regression": ScheduleRegression,
    }

    overall_errors = {}

    for schedule_name, model_name in schedule_models.items():
        if not data.get(schedule_name) or not isinstance(data.get(schedule_name), list):
            logging.warning(f"No valid data for schedule '{schedule_name}'. Skipping.")
            continue

        validation_errors = []
        validated_items = []

        for idx, item in enumerate(data.get(schedule_name)):
            try:
                validated_item = ScheduleItem(**item)
                validated_items.append(validated_item)
                logging.info(
                    f"Validated item {idx + 1} in '{schedule_name}': {validated_item}"
                )
            except ValidationError as e:
                logging.error(
                    f"Validation error in item {idx + 1} of '{schedule_name}': {e}"
                )
                validation_errors.append({"item_index": idx + 1, "errors": e.errors()})

        if validation_errors:
            overall_errors[schedule_name] = validation_errors
            continue  # Пропускаем сохранение этого графика

        try:
            for item in validated_items:
                new_schedule = model_name(
                    calc_id=item.calc_id,
                    payment_date=item.payment_date,
                    payment_date_ru=item.payment_date.strftime("%d.%m.%Y"),
                    leas_payment_amount=item.leas_payment_amount,
                    leas_payment_amount_str=validate_item_price(
                        str(item.leas_payment_amount)
                    ),
                    early_repayment_amount=item.early_repayment_amount,
                    early_repayment_amount_str=validate_item_price(
                        str(item.early_repayment_amount)
                    ),
                )
                db.session.add(new_schedule)

            db.session.commit()
            logging.info(
                f"Schedule '{schedule_name}' successfully uploaded and committed to the database."
            )

        except Exception as e:
            db.session.rollback()
            logging.exception(
                f"An error occurred while uploading schedule '{schedule_name}'."
            )
            overall_errors[schedule_name] = {
                "error": f"Database error. Description: {e}"
            }
            continue  # Или вернуть ошибку сразу

    if overall_errors:
        return (
            jsonify(
                {
                    "message": "Some schedules were not uploaded",
                    "errors": overall_errors,
                }
            ),
            207,
        )

    return jsonify({"message": "All schedules successfully uploaded"}), 201


def post_request_leas_calc(data, calc_id) -> dict:
    url = f"{URL_XLSX_API}/api/start-full"
    headers = {"Content-Type": "application/json"}
    json_data = data | {"calc_id": calc_id}

    response: dict = requests.post(url, headers=headers, json=json_data).json()
    return response


def upload_main_info(data: dict):
    """
    Uploads main calculation data to the database.
    """
    logging.info("Received data for main info upload.")

    main_info_models = {
        "annuity_data": MainAnnuity,
        "differentiated_data": MainDifferentiated,
        "regression_data": MainRegression,
    }

    overall_errors = {}

    for main_info_name, model_class in main_info_models.items():
        main_info_data = data.get(main_info_name)
        if not main_info_data:
            logging.warning(f"No data provided for '{main_info_name}'. Skipping.")
            continue

        try:
            # Validate data using Pydantic
            validated_data = MainInfoItem(**main_info_data)
            logging.info(f"Validated data for '{main_info_name}': {validated_data}")

            # Create model instance
            new_main_info = model_class(
                calc_id=validated_data.calc_id,
                lease_agreement_amount=validated_data.lease_agreement_amount,
                lease_agreement_amount_str=validate_item_price(
                    str(validated_data.lease_agreement_amount)
                ),
                vat_refund=validated_data.vat_refund,
                vat_refund_str=validate_item_price(str(validated_data.vat_refund)),
                save_income_tax=validated_data.save_income_tax,
                save_income_tax_str=validate_item_price(
                    str(validated_data.save_income_tax)
                ),
                total_cost=validated_data.total_cost,
                total_cost_str=validate_item_price(str(validated_data.total_cost)),
                redemption_value=validated_data.redemption_value,
                redemption_value_str=validate_item_price(
                    str(validated_data.redemption_value)
                ),
                transaction_processing_fee=validated_data.transaction_processing_fee,
                transaction_processing_fee_str=validate_item_price(
                    str(validated_data.transaction_processing_fee)
                ),
                company_margin=validated_data.company_margin,
                company_margin_str=validate_item_price(
                    str(validated_data.company_margin)
                ),
                effective_rate=validated_data.effective_rate,
                effective_rate_str=validate_item_price(
                    str(validated_data.effective_rate)
                ),
                increase_rate=validated_data.increase_rate,
                increase_rate_str=validate_item_price(
                    str(validated_data.increase_rate)
                ),
            )

            db.session.add(new_main_info)
            db.session.commit()
            logging.info(f"Data for '{main_info_name}' successfully uploaded.")

        except ValidationError as ve:
            logging.error(f"Validation error for '{main_info_name}': {ve}")
            overall_errors[main_info_name] = ve.errors()
            db.session.rollback()

        except SQLAlchemyError as sae:
            logging.error(f"Database error for '{main_info_name}': {sae}")
            overall_errors[main_info_name] = "Database error occurred."
            db.session.rollback()

        except Exception as e:
            logging.exception(
                f"An unexpected error occurred for '{main_info_name}'. Description: {e}"
            )
            overall_errors[main_info_name] = "An unexpected error occurred."
            db.session.rollback()

    if overall_errors:
        return (
            jsonify(
                {
                    "message": "Some main info data were not uploaded.",
                    "errors": overall_errors,
                }
            ),
            207,
        )  # 207 Multi-Status

    return jsonify({"message": "All main info data successfully uploaded."}), 201


def post_request_upload_file_site(file_name: str, calc_id: int | str) -> dict:
    url = f"{URL_XLSX_API}/api/upload-file-site"
    headers = {"Content-Type": "application/json"}
    json_data = {"file_name": file_name, "calc_id": calc_id}
    try:
        logging.info(f"Отправляем POST запрос на {url} с данными: {json_data}")
        response: dict = requests.post(url, headers=headers, json=json_data).json()
    except Exception as e:
        logging.error(f"An error occurred while uploading the file: {e}")
        response = {"error": "An error occurred while uploading the file."}
    return response
