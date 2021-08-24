import asyncio
import shelve
from dataclasses import asdict
from typing import Dict

import pytest

from src.resellers.models import Reseller
from src.resellers.schemas import ResellerIn


class FakeShelveRepository:
    def __init__(self, session):
        self.id = 1
        session["resellers"] = []
        self.session = session["resellers"]

    async def add(self, reseller: Reseller) -> Dict:
        await asyncio.sleep(0.3)

        data = {"id": self.id, **asdict(reseller)}
        self.session.append({self.id: data})
        self.id += 1
        return data

    async def get(self, pk: int) -> Dict:
        await asyncio.sleep(0.3)

        for result in self.session:
            if result.get(pk):
                return result[pk]
        return {}


@pytest.fixture
def reseller_model():
    return Reseller(
        "First_Name",
        "Last_Name",
        "123.456.789-10",
        "test@test.com",
        "Pwd@123",
    )


@pytest.fixture
def resellerin_schema():
    return ResellerIn(
        first_name="First_Name",
        last_name="Last_Name",
        password="Pwd@123",
        cpf="123.456.789-10",
        email="test@test.com",
    )


@pytest.fixture
def shelve_session():
    session = shelve.open("test.db", writeback=True)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def fake_repository(shelve_session):
    return FakeShelveRepository(shelve_session)
