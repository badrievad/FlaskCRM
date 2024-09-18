import json
from datetime import datetime, date
from logger import logging


class DealsValidate:
    """class for deal validation"""

    def __init__(self, json_response):
        self._data: dict = json_response

    @property
    def get_company_name(self) -> str:
        name: str = self._data.get("title", "")
        formatted_name: str = name.split(",")[0].strip()
        return formatted_name

    @property
    def get_company_based_on(self) -> str:
        try:
            format_date_reg = self.get_company_reg_date.strftime("%d.%m.%Y")
        except Exception as e:
            logging.error(f"Error: {e}")
            format_date_reg = ""

        based_on = (
            "Устава"
            if len(self.get_company_inn) == 10
            else f"выписки Листа записи "
            f"Единого государственного реестра индивидуальных предпринимателей от {format_date_reg}"
        )
        return based_on

    @property
    def get_name_without_special_symbols(self) -> str:
        forbidden_chars: set = {"\\", "/", ":", "*", "?", '"', "<", ">", "|"}
        name_without_special_symbols: str = "".join(
            char for char in self.get_company_name if char not in forbidden_chars
        )
        return name_without_special_symbols

    @property
    def get_company_inn(self) -> str:
        info_json: json = self._data.get("info")
        if info_json:
            info: dict = json.loads(info_json)
        else:
            info: dict = {}
        return info.get("data", {}).get("inn", "")

    @property
    def get_company_ogrn(self) -> str:
        info_json: json = self._data.get("info")
        if info_json:
            info: dict = json.loads(info_json)
        else:
            info: dict = {}
        return info.get("data", {}).get("ogrn", "")

    @property
    def get_company_kpp(self) -> str:
        info_json: json = self._data.get("info")
        if info_json:
            info: dict = json.loads(info_json)
        else:
            info: dict = {}
        return info.get("data", {}).get("kpp", "-")

    @property
    def get_company_okato(self) -> str:
        info_json: json = self._data.get("info")
        if info_json:
            info: dict = json.loads(info_json)
        else:
            info: dict = {}
        return info.get("data", {}).get("okato", "-")

    @property
    def get_company_address(self) -> str:
        info_json: json = self._data.get("info")
        if info_json:
            info: dict = json.loads(info_json)
        else:
            info: dict = {}
        return info.get("data", {}).get("address", {}).get("unrestricted_value", "")

    @property
    def get_company_signer(self) -> str:
        info_json: json = self._data.get("info")
        if info_json:
            info: dict = json.loads(info_json)
        else:
            info: dict = {}

        management: str = info.get("data", {}).get("management", {}).get("name", "")
        if management:
            return management

        return info.get("data", {}).get("name", {}).get("full", "")

    @property
    def get_company_reg_date(self) -> date | None:
        info_json: str = self._data.get("info")
        if info_json:
            info: dict = json.loads(info_json)
        else:
            info: dict = {}
        ogrn_date_ms = info.get("data", {}).get("ogrn_date", "")
        if ogrn_date_ms:
            try:
                ogrn_date_s = int(ogrn_date_ms) / 1000
                dt = datetime.fromtimestamp(ogrn_date_s)
                return dt.date()  # Возвращаем объект datetime.date
            except (ValueError, TypeError):
                return None
        else:
            return None
