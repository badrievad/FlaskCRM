from datetime import datetime

from log_conf import logger

from ... import db
from ..risk_department.models import RiskDepartment


def process_risk_decision(deal_id, decision):
    # Проверяем корректность решения
    if decision not in ["approve", "send_to_committee", "reject"]:
        return False, "Некорректное решение."

    # Получаем или создаем запись RiskDepartment для данного deal_id
    risk_record = RiskDepartment.query.filter_by(deal_id=deal_id).first()
    if not risk_record:
        risk_record = RiskDepartment(deal_id=deal_id)
        db.session.add(risk_record)

    # Обновляем поля записи
    risk_record.decision = decision
    risk_record.decision_time = datetime.now()

    # Сохраняем изменения в базе данных
    try:
        # Формируем сообщение для пользователя
        if decision == "approve":
            risk_record.decision_icon = "https://img.icons8.com/doodle/48/ok.png"
            message = "Сделка одобрена."
        elif decision == "send_to_committee":
            risk_record.decision_icon = (
                "https://img.icons8.com/doodle/48/microsoft-teams-2019.png"
            )
            message = "Сделка отправлена на инвестиционный комитет."
        elif decision == "reject":
            risk_record.decision_icon = "https://img.icons8.com/doodle/48/cancel-2.png"
            message = "По сделке отказано."

        db.session.commit()
        return True, message
    except Exception as e:
        db.session.rollback()
        logger.error(f"Ошибка при сохранении решения в БД: {e}")
        return False, "Ошибка сохранения решения."


def get_decision(deal_id) -> dict[str, str] | None:
    # Получаем решение из базы данных
    risk_record = RiskDepartment.query.filter_by(deal_id=deal_id).first()

    if not risk_record:
        return None

    decision = risk_record.decision if risk_record else None

    # Преобразуем код решения в текст
    decision_mapping = {
        "approve": "Сделка одобрена.",
        "send_to_committee": "Сделка отправлена на инвестиционный комитет.",
        "reject": "По сделке отказано.",
    }
    decision_text = decision_mapping.get(decision, "") if decision else ""
    decision_icon = risk_record.decision_icon if risk_record else ""
    decision_time = (
        risk_record.decision_time.strftime("%d.%m.%Y, %H:%M") if risk_record else ""
    )

    return {
        "decision": decision,
        "decision_text": decision_text,
        "decision_icon": decision_icon,
        "decision_time": decision_time,
    }


def delete_risk_decision(deal_id):
    # Получаем запись RiskDepartment по deal_id
    risk_record = RiskDepartment.query.filter_by(deal_id=deal_id).first()
    if not risk_record:
        return False, "Решение не найдено."

    # Удаляем запись из базы данных
    try:
        db.session.delete(risk_record)
        db.session.commit()
        return True, "Решение успешно удалено."
    except Exception as e:
        db.session.rollback()
        logger.error(f"Ошибка при удалении решения из БД: {e}")
        return False, "Ошибка при удалении решения."
