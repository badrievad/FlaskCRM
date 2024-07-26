from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class Tranche(BaseModel):
    size: float
    rate: float = Field(alias="interestRate")
    fee: float
    own_fee: float = Field(alias="ownFee")
    credit_date: str = Field(alias="creditDate")
    payment_date: str = Field(alias="paymentDate")

    @field_validator("fee", "own_fee", mode="before")
    def parse_float_with_comma(cls, value) -> float:
        if isinstance(value, str):
            return float(value.replace(",", "."))
        return value


class Tranches(BaseModel):
    tranche1: Tranche
    tranche2: Tranche
    tranche3: Tranche
    tranche4: Tranche
    tranche5: Tranche


class ValidateFields(BaseModel):
    item_type: str = Field(alias="itemType")
    item_price: float = Field(alias="itemPrice")
    interest_rate: float = Field(alias="interestRate")
    item_name: str = Field(alias="itemName", default="-")
    currency: str
    foreign_cost: float = Field(alias="foreignCost")
    initial_payment: float = Field(alias="initialPayment")
    credit: float
    credit_term: int = Field(alias="creditTerm")
    bank_commission: float = Field(alias="bankCommission")
    insurance_casko: float = Field(alias="insuranceCasko")
    insurance_osago: float = Field(alias="insuranceOsago")
    health_insurance: float = Field(alias="healthInsurance")
    other_insurance: float = Field(alias="otherInsurance")
    agent_commission: float = Field(alias="agentCommission")
    manager_bonus: float = Field(alias="managerBonus")
    tracker: float
    mayak: float
    fedresurs: float
    gsm: float
    mail: float
    tranches: Tranches

    class Config:
        populate_by_name = True
        allow_population_by_alias = True
