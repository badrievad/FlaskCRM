import json


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
    def get_name_without_special_symbols(self) -> str:
        forbidden_chars = {"\\", "/", ":", "*", "?", '"', "<", ">", "|"}
        name_without_special_symbols = "".join(
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
