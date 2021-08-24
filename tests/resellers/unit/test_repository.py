import pytest

from src.resellers.repository import Repository


class TestRepository:
    def test_should_be_a_repository(self, fake_repository):
        assert isinstance(fake_repository, Repository)

    @pytest.mark.asyncio
    async def test_should_add_reseller(
        self, shelve_session, fake_repository, reseller_model
    ):
        result = await fake_repository.add(reseller_model)
        assert len(shelve_session["resellers"]) == 1
        assert result["id"] == 1

    @pytest.mark.asyncio
    async def test_should_get_reseller(self, fake_repository, reseller_model):
        result = await fake_repository.add(reseller_model)

        reseller_result = await fake_repository.get(result["id"])
        assert result == reseller_result
