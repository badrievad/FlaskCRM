import pytest
from app.deal.other_utils import validate_item_price


def test_validate_item_price():
    assert validate_item_price("123") == "123,00"
    assert validate_item_price("1231    ") == "1 231,00"
    assert validate_item_price("12231.24") == "12 231,24"
    assert validate_item_price("12231,24") == "12 231,24"
    assert validate_item_price(" 1 222 231.24") == "1 222 231,24"
    assert validate_item_price("123,") == "123,00"
    assert validate_item_price("123.") == "123,00"


def test_empty_validate_item_price():
    assert validate_item_price("") == "0,00"


def test_wrong_input_validate_item_price():
    with pytest.raises(
        ValueError, match="Input contains letters, which is not allowed."
    ):
        validate_item_price("123a")
