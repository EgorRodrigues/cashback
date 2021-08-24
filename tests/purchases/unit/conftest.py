from datetime import datetime
from decimal import Decimal

import pytest

from src.purchases.models import Purchase, Status


@pytest.fixture
def purchase_model():
    return Purchase(
        code="100500",
        amount=Decimal(1000),
        date=datetime(year=2021, month=8, day=23, hour=23, minute=58),
        cpf_reseller="123.123.123-23",
        status=Status.IN_VALIDATION,
    )
