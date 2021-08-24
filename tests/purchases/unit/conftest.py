import asyncio
import shelve
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

import pytest

from src.purchases.models import Purchase, Status
from src.purchases.schemas import PurchaseIn


class FakeShelveRepository:
    def __init__(self, session):
        self.id = 1
        session["purchases"] = []
        self.session = session["purchases"]

    async def add(self, purchase: Purchase) -> Dict:
        await asyncio.sleep(0.3)

        data = {"id": self.id, **asdict(purchase)}
        self.session.append({self.id: data})
        self.id += 1
        return data

    async def get(self, pk: int) -> Dict:
        await asyncio.sleep(0.3)

        for result in self.session:
            if result.get(pk):
                return result[pk]
        return {}

    async def update(self, pk: int, purchase: Purchase) -> bool:
        data = {"id": pk, **asdict(purchase)}
        for result in self.session:
            if result.get(pk):
                result[pk] = data
                return 1
        return 0

    async def delete(self, pk: int) -> bool:
        result = True
        return bool(result)

    async def list_purchases(self, reseller_id: Optional[int] = None) -> List:
        result = []
        return result


@pytest.fixture
def purchase_model():
    return Purchase(
        code="100500",
        amount=Decimal(1000),
        date=datetime(year=2021, month=8, day=23, hour=23, minute=58),
        cpf_reseller="123.123.123-23",
        status=Status.IN_VALIDATION,
    )


@pytest.fixture
def fake_repository(shelve_session):
    return FakeShelveRepository(shelve_session)


@pytest.fixture
def purchasein_schema():
    return PurchaseIn(
        code="500100",
        amount=Decimal(1500.00),
        date=datetime(
            year=2021, month=8, day=25, hour=12, minute=10, second=0
        ),
        cpf_reseller="123.123.123-23",
        status=Status.IN_VALIDATION,
    )
