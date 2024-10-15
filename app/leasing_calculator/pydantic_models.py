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
    payment_deferment: int = Field(alias="paymentDeferment", default=0)

    @field_validator("fee", "own_fee", mode="before")
    def parse_float_with_comma(cls, value) -> float:  # noqa
        if isinstance(value, str):
            return float(value.replace(",", ".").replace(" ", ""))
        return value

    @field_validator("rate", mode="before")
    def check_empty_rate(cls, value):  # noqa
        if value in ("", None, float("nan"), "0", "0.0", "0.00", "0,0", "0,00"):
            return 20.0
        return value

    @field_validator("fee", mode="before")
    def check_empty_fee(cls, value):  # noqa
        if value in ("", None, float("nan"), "0", "0.0", "0.00", "0,0", "0,00"):
            return 4.85
        return value

    @field_validator("own_fee", mode="before")
    def check_empty_own_fee(cls, value):  # noqa
        if value in ("", None, float("nan"), "0", "0.0", "0.00", "0,0", "0,00"):
            return 20.0
        return value

    @field_validator("size", mode="before")
    def check_empty_size(cls, value):  # noqa
        if value in ("", None, float("nan"), "0", "0.0", "0.00", "0,0", "0,00"):
            return 0.0
        return value

    @field_validator("payment_deferment", mode="before")
    def check_empty_payment_deferment(cls, value):  # noqa
        if value in ("", None, float("nan"), "0", "0.0", "0.00", "0,0", "0,00"):
            return 0
        return value

    @field_validator("credit_date", mode="before")
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


class Insurance(BaseModel):
    casko: float = 0.0
    osago: float = 0.0
    health: float = 0.0
    other: float = 0.0

    @field_validator(
        "casko", "osago", "health", "other", mode="before", check_fields=False
    )
    def parse_float_with_comma(cls, value):  # noqa
        if value in ("", None, float("nan")):
            return 0.0
        if isinstance(value, str):
            return float(value.replace(",", ".").replace(" ", ""))
        return value


class Insurances(BaseModel):
    insurance1: Insurance
    insurance2: Insurance
    insurance3: Insurance
    insurance4: Insurance
    insurance5: Insurance


class ValidateFields(BaseModel):
    item_type: str = Field(alias="itemType")
    item_year: int = Field(alias="itemYear", default=datetime.now().year)
    item_condition: str = Field(alias="itemCondition")
    allocate_vat: str = Field(alias="vat")
    allocate_deposit: str = Field(alias="deposit")
    allocate_redemption: str = Field(alias="redemption")
    item_price: float = Field(alias="itemPrice", default=0.0)
    item_name: str = Field(alias="itemName", default="Отсутствует наименование ПЛ")
    currency: str
    foreign_price: float = Field(alias="foreignCost", default=0.0)
    initial_payment: float = Field(alias="initialPayment", default=0.0)
    credit_sum: float = Field(alias="creditSum", default=0.0)
    credit_term: int = Field(alias="srokCredita", default=1)
    agreement_term: int = Field(alias="creditTerm", default=1)
    reduce_percent: int = Field(alias="reducePercent", default=10)
    leas_day: int = Field(alias="leasDay", default=20)
    service_life: int = Field(alias="serviceLife", default=37)
    amortization: str = Field(alias="amortization", default="")
    nds_size: int = Field(alias="ndsSize", default=20)
    bank_commission: float = Field(alias="bankCommission", default=0.0)
    lkmb_commission: float = Field(alias="lkmbCommission", default=0.0)
    insurances: Insurances
    agent_commission: float = Field(alias="agentCommission", default=0.0)
    manager_bonus: float = Field(alias="managerBonus", default=0.0)
    tracker: float = 0.0
    mayak: float = 0.0
    fedresurs: float = 0.0
    gsm: float = 0.0
    mail: float = 0.0
    depr_transport: float = Field(alias="deprTransport", default=0.0)
    travel: float = 0.0
    stationery: float = 0.0
    internet: float = 0.0
    pledge: float = 0.0
    bank_pledge: float = Field(alias="bankPledge", default=0.0)
    express: float = 0.0
    egrn: float = 0.0
    egrul: float = 0.0
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
        "lkmb_commission",
        "agent_commission",
        "manager_bonus",
        "tracker",
        "mayak",
        "fedresurs",
        "gsm",
        "mail",
        "depr_transport",
        "travel",
        "stationery",
        "internet",
        "pledge",
        "bank_pledge",
        "express",
        "egrn",
        "egrul",
        mode="before",
    )
    def check_empty_price(cls, value):  # noqa
        if value in ("", None, float("nan"), "NaN"):
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

    @field_validator("item_year", mode="before")
    def chech_year(cls, value):  # noqa
        if value in ("", None, float("nan")):
            return datetime.now().year
        return value

    class Config:
        populate_by_name = True
        allow_population_by_alias = True
