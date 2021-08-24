from typing import List

import pytest

from src.purchases.schemas import PurchaseInDB, PurchaseOut
from src.purchases.services import PurchaseService


class TestService:
    @pytest.mark.asyncio
    async def test_should_prepare_create(
        self, shelve_session, fake_repository, purchasein_schema
    ):
        assert len(shelve_session["purchases"]) == 0
        purchase_in_db = await PurchaseService(fake_repository).prepare_create(
            purchasein_schema
        )
        assert len(shelve_session["purchases"]) == 1
        assert isinstance(purchase_in_db, PurchaseInDB)

    @pytest.mark.asyncio
    async def test_should_prepare_get(
        self, fake_repository, purchasein_schema
    ):
        await PurchaseService(fake_repository).prepare_create(
            purchasein_schema
        )
        purchase_out = await PurchaseService(fake_repository).prepare_get(1)
        assert isinstance(purchase_out, PurchaseOut)
        assert purchasein_schema.code == purchase_out.code
        assert purchasein_schema.cpf_reseller == purchase_out.cpf_reseller

    @pytest.mark.asyncio
    @pytest.mark.parametrize("pk", [1])
    async def test_prepare_update(
        self, fake_repository, pk, purchasein_schema
    ):
        await PurchaseService(fake_repository).prepare_create(
            purchasein_schema
        )
        purchase_out = await PurchaseService(fake_repository).prepare_update(
            pk, purchasein_schema
        )
        assert purchase_out == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("pk", [1])
    async def test_prepare_delete(
        self, fake_repository, pk, purchasein_schema
    ):
        await PurchaseService(fake_repository).prepare_create(
            purchasein_schema
        )
        purchase_out = await PurchaseService(fake_repository).prepare_delete(
            pk
        )
        assert purchase_out is True

    @pytest.mark.asyncio
    @pytest.mark.parametrize("fake_reseller_id", [1])
    async def test_prepare_list(
        self, fake_repository, purchasein_schema, fake_reseller_id
    ):
        await PurchaseService(fake_repository).prepare_create(
            purchasein_schema
        )
        purchase_list = await PurchaseService(fake_repository).prepare_list(
            fake_reseller_id
        )
        assert isinstance(purchase_list, List)
