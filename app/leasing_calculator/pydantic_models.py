from datetime import datetime
from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class Tranche(BaseModel):
    size: float = 0.0
    rate: float = Field(alias="interestRate", default=0.0)
    fee: float = 0.0
    own_fee: float = Field(alias="ownFee", default=0.0)
    credit_date: str = Field(
        alias="creditDate", default_factory=lambda: datetime.now().strftime("%Y-%m-%d")
    )
    payment_date: str = Field(
        alias="paymentDate", default_factory=lambda: datetime.now().strftime("%Y-%m-%d")
    )

    @field_validator("fee", "own_fee", mode="before")
    def parse_float_with_comma(cls, value) -> float:  # noqa
        if isinstance(value, str):
            return float(value.replace(",", "."))
        return value

    @field_validator("size", "rate", "fee", "own_fee", mode="before")
    def check_empty(cls, value):  # noqa
        if value in ("", None, float("nan")):
            return 0.0
        return value

    @field_validator("credit_date", "payment_date", mode="before")
    def set_default_date(cls, value):  # noqa
        if not value:
            return datetime.now().strftime("%Y-%m-%d")
        return value


class Tranches(BaseModel):
    tranche1: Tranche
    tranche2: Tranche
    tranche3: Tranche
    tranche4: Tranche
    tranche5: Tranche


class ValidateFields(BaseModel):
    item_type: str = Field(alias="itemType")
    item_price: float = Field(alias="itemPrice", default=0.0)
    item_name: str = Field(alias="itemName", default="Отсутствует наименование ПЛ")
    currency: str
    foreign_price: float = Field(alias="foreignCost", default=0.0)
    initial_payment: float = Field(alias="initialPayment", default=0.0)
    credit_sum: float = Field(alias="creditSum", default=0.0)
    credit_term: int = Field(alias="creditTerm", default=1)
    bank_commission: float = Field(alias="bankCommission", default=0.0)
    insurance_casko: float = Field(alias="insuranceCasko", default=0.0)
    insurance_osago: float = Field(alias="insuranceOsago", default=0.0)
    health_insurance: float = Field(alias="healthInsurance", default=0.0)
    other_insurance: float = Field(alias="otherInsurance", default=0.0)
    agent_commission: float = Field(alias="agentCommission", default=0.0)
    manager_bonus: float = Field(alias="managerBonus", default=0.0)
    tracker: float = 0.0
    mayak: float = 0.0
    fedresurs: float = 0.0
    gsm: float = 0.0
    mail: float = 0.0
    input_period: str = Field(
        alias="inputPeriod", default_factory=lambda: datetime.now().strftime("%Y-%m-%d")
    )
    tranches: Tranches

    @field_validator("item_name", mode="before")
    def check_empty_name(cls, value):  # noqa
        if value in ("", None, float("nan")):
            return "Отсутствует наименование ПЛ"
        return value

    @field_validator(
        "item_price",
        "foreign_price",
        "initial_payment",
        "credit_sum",
        "bank_commission",
        "insurance_casko",
        "insurance_osago",
        "health_insurance",
        "other_insurance",
        "agent_commission",
        "manager_bonus",
        "tracker",
        "mayak",
        "fedresurs",
        "gsm",
        "mail",
        mode="before",
    )
    def check_empty_price(cls, value):  # noqa
        if value in ("", None, float("nan")):
            return 0.0
        return value

    @field_validator("input_period", mode="before")
    def set_default_date(cls, value):  # noqa
        if not value:
            return datetime.now().strftime("%Y-%m-%d")
        return value

    @field_validator("credit_term", mode="before")
    def check_term(cls, value):  # noqa
        if value in ("", None, float("nan")):
            return 1
        return value

    class Config:
        populate_by_name = True
        allow_population_by_alias = True
