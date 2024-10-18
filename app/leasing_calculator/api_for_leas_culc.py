import requests

from pydantic import BaseModel, ValidationError, field_validator, Field
from datetime import date
from flask import jsonify
from logger import logging

from .models import ScheduleAnnuity, ScheduleDifferentiated, ScheduleRegression
from .other_utils import validate_item_price
from .. import db
from ..config import URL_XLSX_API


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
