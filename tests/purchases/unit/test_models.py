from datetime import datetime
from decimal import Decimal

import pytest

from src.purchases.models import Purchase, Status


class TestPurchase:
    def test_should_create_reseller_instance(self, purchase_model):
        assert isinstance(purchase_model, Purchase)

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (999.99, 99.999),
            (1000.00, 150.00),
            (1499.99, 224.9985),
            (1500.00, 300.00),
        ],
    )
    def test_should_return_values_calculated_according_to_the_cashback_rule(
        self, test_input, expected
    ):
        purchase_model = Purchase(
            code="100500",
            amount=Decimal(test_input),
            date=datetime(year=2021, month=8, day=23, hour=23, minute=58),
            cpf_reseller="123.123.123-23",
            status=Status.IN_VALIDATION,
        )
        assert purchase_model.cashback.amount.quantize(
            Decimal("0.0001")
        ) == Decimal(expected).quantize(Decimal("0.0001"))

    @pytest.mark.parametrize(
        "cpf,status_in,status_out",
        [
            ("123.123.123-23", Status.IN_VALIDATION, Status.IN_VALIDATION),
            ("123.123.123-23", Status.APPROVED, Status.IN_VALIDATION),
            ("153.509.460-56", Status.IN_VALIDATION, Status.APPROVED),
        ],
    )
    def test_should_return_status_validation(self, cpf, status_in, status_out):
        purchase_model = Purchase(
            code="100500",
            amount=Decimal(1000.00),
            date=datetime(year=2021, month=8, day=23, hour=23, minute=58),
            cpf_reseller=cpf,
            status=status_in,
        )
        assert purchase_model.status == status_out
