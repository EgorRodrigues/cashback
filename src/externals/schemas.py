from decimal import Decimal

from pydantic import BaseModel


class AccruedCashbackOut(BaseModel):
    credit: Decimal

    @staticmethod
    def from_dict(obj) -> "AccruedCashbackOut":
        return AccruedCashbackOut(credit=obj["body"]["credit"])


class AccruedCashbackIn(BaseModel):
    cpf_reseller: str
