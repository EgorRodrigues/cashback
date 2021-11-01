from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List

from prettyconf import config


class Status(str, Enum):
    IN_VALIDATION = "Em Validação"
    APPROVED = "Aprovado"
    DENIED = "Negado"


@dataclass
class Cashback:
    percent: Decimal
    amount: Decimal

    def __composite_values__(self):
        return self.percent, self.amount

    def __repr__(self):
        return "Cashback(percent=%s, amount=%s)" % (self.percent, self.amount)

    def __eq__(self, other):
        return (
            isinstance(other, Cashback)
            and other.percent == self.percent
            and other.amount == self.amount
        )

    def __ne__(self, other):
        return not self.__eq__(other)


@dataclass
class Purchase:
    code: str
    amount: Decimal
    date: datetime
    cashback: Cashback = field(init=False)
    status: Status = Status.IN_VALIDATION.value

    def __post_init__(self):
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


@dataclass
class Reseller:
    cpf: str
    purchases: List[Purchase]

    def add_purchase(self, purchase: Purchase) -> None:
        cpf_list = config("LIST_APPROVED_CPF", cast=config.eval)
        if self.cpf in cpf_list:
            purchase.status = Status.APPROVED
        else:
            purchase.status = Status.IN_VALIDATION
        self.purchases.append(purchase)
