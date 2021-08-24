from datetime import datetime
from decimal import Decimal

import pytest

from src.purchases.models import Purchase, Status
from src.purchases.repository import Repository


class TestRepository:
    def test_should_be_a_repository(self, fake_repository):
        assert isinstance(fake_repository, Repository)

    @pytest.mark.asyncio
    async def test_should_add_purchase(
        self, shelve_session, fake_repository, purchase_model
    ):
        result = await fake_repository.add(purchase_model)
        assert len(shelve_session["purchases"]) == 1
        assert result["id"] == 1

    @pytest.mark.asyncio
    async def test_should_get_purchase(self, fake_repository, purchase_model):
        result = await fake_repository.add(purchase_model)

        purchase_result = await fake_repository.get(result["id"])
        assert result == purchase_result

    @pytest.mark.asyncio
    @pytest.mark.parametrize("pk", [1])
    async def test_should_update_purchase(
        self, fake_repository, pk, purchase_model
    ):
        await fake_repository.add(purchase_model)

        purchase_update = Purchase(
            code="500100",
            amount=Decimal(1500),
            date=datetime(year=2021, month=8, day=24, hour=23, minute=58),
            cpf_reseller="123.123.123-00",
            status=Status.IN_VALIDATION,
        )

        purchase_result = await fake_repository.update(pk, purchase_update)
        assert purchase_result
