from typing import Any

from pydantic import BaseModel, ValidationError, field_validator, Field
from datetime import date

from .models import CalculateResultSchedule
from .. import db
from flask import jsonify
from logger import logging


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


def upload_schedule(data: Any):
    """
    Записывает в БД графики из расчетов Димы
    """
    logging.info("Received data for schedule upload.")

    if not data or not isinstance(data, list):
        logging.error("Invalid data format received. Expected a list of schedules.")
        return (
            jsonify({"error": "Invalid data format. Expected a list of schedules."}),
            400,
        )

    try:
        validated_items = []
        for idx, item in enumerate(data):
            try:
                validated_item = ScheduleItem(**item)
                validated_items.append(validated_item)
                logging.info(f"Validated item {idx + 1}: {validated_item}")
            except ValidationError as e:
                logging.error(f"Validation error in item {idx + 1}: {e}")
                return jsonify({"error": e.errors(), "item_index": idx + 1}), 400

        for item in validated_items:
            new_schedule = CalculateResultSchedule(
                calc_id=item.calc_id,
                payment_date=item.payment_date,
                leas_payment_amount=item.leas_payment_amount,
                early_repayment_amount=item.early_repayment_amount,
            )
            db.session.add(new_schedule)

        db.session.commit()
        logging.info(
            "All schedules successfully uploaded and committed to the database."
        )
        return jsonify({"message": "Schedules successfully uploaded"}), 201

    except Exception as e:
        db.session.rollback()
        logging.error("An unexpected error occurred while uploading schedules.")
        logging.error(e)
        return (
            jsonify({"error": "An unexpected error occurred.", "details": str(e)}),
            500,
        )
