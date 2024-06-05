import json


class DealsValidate:
    """class for deal validation"""

    def __init__(self, json_response):
        self._data: dict = json_response

    @property
    def get_company_name(self) -> str:
        return self._data.get("title", "")

    @property
    def get_company_inn(self) -> str:
        info_json: json = self._data.get("info")
        if info_json:
            info: dict = json.loads(info_json)
        else:
            info: dict = {}
        return info.get("data", {}).get("inn", "")
