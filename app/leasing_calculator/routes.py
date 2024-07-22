import os

from pathlib import Path
from sqlalchemy import desc
from . import leas_calc_bp
from .api_cb_currency import ApiCentralBank
from .other_utils import ValidateFields
from .. import db, cache
from ..leasing_calculator.models import LeasCalculator, LeasingItem
from ..leasing_calculator.celery_tasks import long_task

from flask import (
    request,
    jsonify,
    render_template,
    url_for,
    current_app,
    send_file,
)
from flask_login import current_user, login_required
from logger import logging


@leas_calc_bp.route("/crm/calculator", methods=["GET"])
@login_required
def get_leasing_calculator() -> render_template:
    # установка фона для пользователя
    user_fon_filename = current_user.fon_url
    user_fon_url = url_for("crm.static", filename=user_fon_filename)

    # список расчетов
    user_login = current_user.login
    calc_list = (
        LeasCalculator.query.filter_by(manager_login=user_login)
        .order_by(desc(LeasCalculator.id))
        .all()
    )
    return render_template(
        "leasing_calculator.html",
        user_fon=user_fon_url,
        calc_list=calc_list,
        login=user_login,
    )


# Эндпоинт для запуска фоновой задачи
@leas_calc_bp.route("/crm/calculator/start-task", methods=["POST"])
def start_task() -> jsonify:
    try:
        data: dict = ValidateFields(request.get_json()).get_dict()
        logging.info(f"Поля из сайта (лизинговый калькулятор): {data}")
        user_login: dict = {"login": current_user.login}
        task = long_task.delay({**user_login, **data})
        return jsonify({"task_id": task.id}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@leas_calc_bp.route("/crm/calculator/status/<task_id>", methods=["GET"])
def get_status(task_id) -> jsonify:
    try:
        task = long_task.AsyncResult(task_id)
        if task.state == "PENDING":
            response = {"state": task.state, "status": "Pending..."}
        elif task.state != "FAILURE":
            response = {"state": task.state, "status": task.info}
            if task.state == "SUCCESS" and task.result:
                response["result"] = {
                    "id": task.result.get("id"),
                    "title": task.result.get("title"),
                    "date_ru": task.result.get("date_ru"),
                    "manager_login": task.result.get("manager_login"),
                    "item_type": task.result.get("item_type"),
                    "item_name": task.result.get("item_name"),
                    "item_price": task.result.get("item_price"),
                    "item_price_str": task.result.get("item_price_str"),
                    "term": task.result.get("term"),
                    "prepaid_expense": task.result.get("prepaid_expense"),
                    "interest_rate": task.result.get("interest_rate"),
                    "full_path_to_file": task.result.get("full_path_to_file"),
                }
        else:
            response = {"state": task.state, "status": str(task.info)}
        current_app.logger.info(f"Task {task_id} status: {response}")
        return jsonify(response)
    except Exception as e:
        current_app.logger.error(f"Error fetching status for task {task_id}: {e}")
        return jsonify({"error": str(e)}), 500


@leas_calc_bp.route("/crm/calculator/delete/<int:calc_id>", methods=["POST"])
def delete_calculation(calc_id) -> jsonify:
    try:
        calc = LeasCalculator.query.filter_by(id=calc_id).first()
        if calc is None:
            return jsonify({"success": False, "message": "Calculation not found"}), 404

        db.session.delete(calc)
        db.session.commit()
        return jsonify({"success": True, "message": "Calculation deleted successfully"})

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "success": False,
                    "message": "An error occurred while deleting the calculation",
                    "error": str(e),
                }
            ),
            500,
        )


@leas_calc_bp.route("/crm/calculator/download/<int:calc_id>", methods=["GET"])
def download_calculation(calc_id):
    logging.info(f"Запрос на скачивание калькулятора (id_{calc_id})")
    try:
        calc = LeasCalculator.query.filter_by(id=calc_id).first()
        if calc is None:
            return jsonify({"success": False, "message": "Calculation not found"}), 404

        file_path = Path(calc.path_to_file) / calc.title
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "File not found"}), 404

        return send_file(
            file_path.resolve(), as_attachment=True, download_name=calc.title
        )

    except Exception as e:
        logging.info(f"Ошибка при скачивании калькулятора: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "An error occurred while downloading the calculation",
                    "error": str(e),
                }
            ),
            500,
        )


@leas_calc_bp.route("/crm/calculator/autocomplete", methods=["GET"])
def autocomplete() -> jsonify:
    query = request.args.get("query", "")
    suggestions = (
        LeasingItem.query.filter(LeasingItem.name.ilike(f"%{query}%")).limit(10).all()
    )
    results = [item.name for item in suggestions]
    return jsonify(results)


@leas_calc_bp.route("/crm/calculator/update/<int:calc_id>", methods=["POST"])
def update_calculation(calc_id) -> jsonify:
    try:
        if not request.is_json:
            logging.error("Request data is not in JSON format")
            return (
                jsonify(
                    {"success": False, "message": "Request data must be in JSON format"}
                ),
                400,
            )
        else:
            logging.info("Request data is in JSON format")

        data = request.get_json()
        logging.info(f"Запрос на обновление калькулятора (id_{calc_id}): {data}")

        calc = LeasCalculator.query.filter_by(id=calc_id).first()
        if calc is None:
            return jsonify({"success": False, "message": "Calculation not found"}), 404

        for key, value in data.items():
            if value == "-":
                continue
            setattr(calc, key, value)

        db.session.commit()

        updated_data = {
            "id": calc.id,
            "item_name": calc.item_name,
            "item_price": calc.item_price_str,
            "item_type": calc.item_type,
            "date_ru": calc.date_ru,
        }

        return jsonify(
            {
                "success": True,
                "message": "Calculation updated successfully",
                "data": updated_data,
            }
        )

    except Exception as e:
        db.session.rollback()
        logging.error(f"Ошибка при обновлении калькулятора: {str(e)}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "An error occurred while updating the calculation",
                    "error": str(e),
                }
            ),
            500,
        )


@leas_calc_bp.route("/crm/calculator/get_exchange_rates", methods=["GET"])
@cache.cached(timeout=600)
def get_exchange_rates() -> jsonify:
    api = ApiCentralBank()
    exchange_rates: dict = api.get_exchange_rates()
    return jsonify(exchange_rates)
