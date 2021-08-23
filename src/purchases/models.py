from dataclasses import InitVar, dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum

from prettyconf import config


class Status(str, Enum):
    IN_VALIDATION = "Em Validação"
    APPROVED = "Aprovado"
    DENIED = "Negado"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class Cashback:
    percent: Decimal
    amount: Decimal


@dataclass
class Purchase:
    code: str
    amount: Decimal
    date: datetime
    cpf_reseller: str
    cashback_percent: InitVar[Decimal]
    cashback_amount: InitVar[Decimal]
    cashback: Cashback = field(init=False)
    status: Status = Status.IN_VALIDATION

    def __post_init__(
        self,
        cashback_percent: Decimal,
        cashback_amount: Decimal,
    ) -> None:
        cpf_list = config("LIST_APPROVED_CPF", cast=config.eval)
        if self.cpf_reseller in cpf_list:
            self.status = Status.APPROVED
        self.cashback = Cashback(cashback_percent, cashback_amount)
        self.calculate_cashback()

    def calculate_cashback(self):
        if self.amount < 1000:
            self.cashback.percent = Decimal(0.1)
            self.cashback.amount = self.amount * self.cashback.percent
        elif self.amount >= 1000 and self.amount > 1500:
            self.cashback.percent = Decimal(0.15)
            self.cashback.amount = self.amount * self.cashback.percent
        else:
            self.cashback.percent = Decimal(0.2)
            self.cashback.amount = self.amount * self.cashback.percent
