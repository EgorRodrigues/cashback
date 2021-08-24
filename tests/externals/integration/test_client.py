import pytest

from src.externals.clients import Client, HTTPXAsyncClient


def test_should_check_if_httpx_client_is_a_client_instance():
    assert isinstance(HTTPXAsyncClient, Client)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_should_get_accrued_cashback_by_client():
    response = await HTTPXAsyncClient.accrued_cashback("fake_cpf")
    accrued_cashback = response["body"]["credit"]
    assert accrued_cashback == 1022
