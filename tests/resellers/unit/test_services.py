import pytest

from src.resellers.schemas import ResellerInDB, ResellerOut
from src.resellers.services import ResellerService


class TestService:
    @pytest.mark.asyncio
    async def test_should_prepare_create(
        self, shelve_session, fake_repository, resellerin_schema
    ):
        assert len(shelve_session["resellers"]) == 0
        reseller_in_db = await ResellerService(fake_repository).prepare_create(
            resellerin_schema
        )
        assert len(shelve_session["resellers"]) == 1
        assert isinstance(reseller_in_db, ResellerInDB)

    @pytest.mark.asyncio
    async def test_should_prepare_get(
        self, fake_repository, resellerin_schema
    ):
        await ResellerService(fake_repository).prepare_create(
            resellerin_schema
        )
        reseller_out = await ResellerService(fake_repository).prepare_get(1)
        assert isinstance(reseller_out, ResellerOut)
        assert resellerin_schema.email == reseller_out.email
        assert resellerin_schema.cpf == reseller_out.cpf
