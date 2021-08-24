from decimal import Decimal

import pytest

from src.externals.clients import HTTPXAsyncClient
from src.externals.schemas import AccruedCashbackOut
from src.externals.services import ExternalsService


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_should_get_accrued_cashback_by_service():
    response = await ExternalsService(
        HTTPXAsyncClient
    ).prepare_accrued_cashback("fake_cpf")
    assert isinstance(response, AccruedCashbackOut)
    assert response.credit == Decimal(2350)
