import pytest

from src.resellers.models import Reseller


@pytest.fixture
def reseller():
    return Reseller(
        "First_Name",
        "Last_Name",
        "123.456.789-10",
        "test@test.com",
        "Pwd@123",
    )
