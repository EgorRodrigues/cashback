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
    cashback: Cashback = field(init=False)
    status: Status = Status.IN_VALIDATION

    def __post_init__(self):
        cpf_list = config("LIST_APPROVED_CPF", cast=config.eval)
        if self.cpf_reseller in cpf_list:
            self.status = Status.APPROVED
        self.calculate_cashback()

    def calculate_cashback(self):

        if self.amount < 1000:
            percent = Decimal(0.1)
            amount = self.amount * percent
        elif 1000 <= self.amount < 1500:
            percent = Decimal(0.15)
            amount = self.amount * percent
        else:
            percent = Decimal(0.2)
            amount = self.amount * percent

        self.cashback = Cashback(percent, amount)
