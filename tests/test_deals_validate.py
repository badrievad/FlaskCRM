import json
import pytest

from app.deal.deals_validate import DealsValidate


@pytest.fixture(
    params=[
        (
            "tests/companies_json/company1.json",
            'ООО "ЛКМБ-РТ"',
            "ООО ЛКМБ-РТ",
            "1655099271",
        ),
        ("tests/companies_json/company2.json", "КНИТУ-КАИ", "КНИТУ-КАИ", "1654003114"),
        (
            "tests/companies_json/company3.json",
            'ФГАОУ ВО "КАЗАНСКИЙ (ПРИВОЛЖСКИЙ) ФЕДЕРАЛЬНЫЙ УНИВЕРСИТЕТ"',
            "ФГАОУ ВО КАЗАНСКИЙ (ПРИВОЛЖСКИЙ) ФЕДЕРАЛЬНЫЙ УНИВЕРСИТЕТ",
            "1655018018",
        ),
        (
            "tests/companies_json/company4.json",
            "ИП Муллабаев Рамис Хусаинович",
            "ИП Муллабаев Рамис Хусаинович",
            "165124723563",
        ),
    ]
)
def company_data(request):
    file_path, expected_name, expected_name_without_special_symbols, expected_inn = (
        request.param
    )
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data, expected_name, expected_name_without_special_symbols, expected_inn


def test_deals_validate(company_data):
    data, expected_name, expected_name_without_special_symbols, expected_inn = (
        company_data
    )
    deals_validate = DealsValidate(data)
    assert deals_validate.get_company_name == expected_name
    assert (
        deals_validate.get_name_without_special_symbols
        == expected_name_without_special_symbols
    )
    assert deals_validate.get_company_inn == expected_inn
