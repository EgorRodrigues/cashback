from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.purchases.models import Purchase as PurchaseModel
from src.purchases.models import Status


class PurchaseBase(BaseModel):
    code: str
    amount: Decimal
    date: datetime
    cpf_reseller: str
    status: Status = Status.IN_VALIDATION.value


class PurchaseIn(PurchaseBase):
    def to_model(self) -> PurchaseModel:
        return PurchaseModel(
            code=self.code,
            amount=self.amount,
            date=self.date,
            cpf_reseller=self.cpf_reseller,
            status=self.status,
        )


class PurchaseOut(PurchaseBase):
    cashback_percent: Decimal
    cashback_amount: Decimal

    @staticmethod
    def from_dict(obj) -> "PurchaseOut":
        return PurchaseOut(
            id=obj["id"],
            code=obj["code"],
            amount=obj["amount"],
            date=obj["date"],
            cpf_reseller=obj["cpf_reseller"],
            cashback_percent=obj["cashback"]["percent"],
            cashback_amount=obj["cashback"]["amount"],
            status=obj["status"],
        )


class PurchaseInDB(PurchaseBase):
    id: int
    cashback_percent: Decimal
    cashback_amount: Decimal

    @staticmethod
    def from_dict(obj) -> "PurchaseInDB":
        return PurchaseInDB(
            id=obj["id"],
            code=obj["code"],
            amount=obj["amount"],
            date=obj["date"],
            cpf_reseller=obj["cpf_reseller"],
            cashback_percent=obj["cashback"]["percent"],
            cashback_amount=obj["cashback"]["amount"],
            status=obj["status"],
        )
