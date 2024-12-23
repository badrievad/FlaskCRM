from datetime import datetime


def format_russian_date(date: datetime) -> str:
    """Форматирует дату в стиле '2 июля 2019 г.'."""
    months = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    }
    return f"{date.day} {months[date.month]} {date.year} г."
