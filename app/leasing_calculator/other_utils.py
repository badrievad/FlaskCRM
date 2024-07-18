import re


def validate_item_price(price: str) -> str:
    # Проверка на наличие букв в строке
    if re.search(r"[a-zA-Z]", price):
        raise ValueError("Input contains letters, which is not allowed.")

    # Проверка на пустую строку
    if not price:
        return "0,00"

    # Удаляем пробелы из строки
    price: str = price.replace(" ", "")

    # Заменяем точку на запятую, если необходимо
    price: str = price.replace(".", ",")

    # Если нет дробной части, добавляем ",00"
    if "," not in price:
        price += ",00"
    else:
        # Убедимся, что дробная часть существует и состоит из двух цифр
        integer_part, fractional_part = price.split(",")
        if fractional_part == "":
            fractional_part = "00"
        elif len(fractional_part) == 1:
            fractional_part += "0"
        elif len(fractional_part) > 2:
            fractional_part = fractional_part[:2]
        price = integer_part + "," + fractional_part

    # Добавляем пробелы как разделители тысяч
    integer_part, fractional_part = price.split(",")
    integer_part_with_spaces: str = re.sub(r"\B(?=(\d{3})+(?!\d))", " ", integer_part)

    # Формируем окончательный результат
    formatted_price: str = integer_part_with_spaces + "," + fractional_part
    return formatted_price


class ValidateFields:
    """Класс для валидации полей формы на странице с калькулятором.
    Если изменится форма на сайте, нужно будет изменить этот класс"""

    def __init__(self, data: dict) -> None:
        self.data = data

    def item_type(self) -> str:
        return self.data.get("itemType", "-")

    def item_price(self) -> str:
        return self.data.get("itemPrice", "-")

    def item_name(self) -> str:
        return self.data.get("itemName", "-")

    def term(self) -> str:
        return self.data.get("term", "-")

    def prepaid_expense(self) -> str:
        return self.data.get("prepaidExpense", "-")

    def interest_rate(self) -> str:
        return self.data.get("interestRate", "-")

    def get_dict(self) -> dict:
        return {
            "item_type": self.item_type(),
            "item_price": self.item_price(),
            "item_name": self.item_name(),
            "term": self.term(),
            "prepaid_expense": self.prepaid_expense(),
            "interest_rate": self.interest_rate(),
        }
