from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.purchases.models import Purchase as PurchaseModel
from src.purchases.models import Status


class PurchaseBase(BaseModel):
    code: str
    amount: Decimal
    date: datetime
    status: Status = Status.IN_VALIDATION.value


class PurchaseIn(PurchaseBase):
    cpf_reseller: str

    def to_model(self) -> PurchaseModel:
        return PurchaseModel(
            code=self.code,
            amount=self.amount,
            date=self.date,
            status=self.status,
        )


class PurchaseOut(PurchaseBase):
    cashback_percent: Decimal
    cashback_amount: Decimal

    @staticmethod
    def from_dict(obj) -> "PurchaseOut":
        return PurchaseOut(
            id=obj.id,
            code=obj.code,
            amount=obj.amount,
            date=obj.date,
            cashback_percent=obj.cashback_percent,
            cashback_amount=obj.cashback_amount,
            status=obj.status,
        )


class PurchaseInDB(PurchaseBase):
    id: int
    cashback_percent: Decimal
    cashback_amount: Decimal

    @staticmethod
    def from_dict(obj) -> "PurchaseInDB":
        return PurchaseInDB(
            id=obj.id,
            code=obj.code,
            amount=obj.amount,
            date=obj.date,
            cashback_percent=obj.cashback_percent,
            cashback_amount=obj.cashback_amount,
            status=obj.status,
        )
