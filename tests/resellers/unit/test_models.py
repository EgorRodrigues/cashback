from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt

from src.resellers.models import Name, Reseller


class TestReseller:
    def test_should_create_reseller_instance(self, reseller):
        assert isinstance(reseller, Reseller)
        assert reseller.cpf == "123.456.789-10"
        assert reseller.email == "test@test.com"

    def test_should_return_full_name_when_getting_the_attribute_name(
        self, reseller
    ):
        assert reseller.name == "First_Name Last_Name"

    def test_should_return_valid_bcrypt_password_when_getting_the_attribute_password(
        self, reseller
    ):
        hashed_password = reseller.password
        str_bcrypt = bcrypt.from_string(hashed_password).to_string()
        assert hashed_password == str_bcrypt

    def test_should_validate_password_when_plain_password_passed(
        self, reseller
    ):
        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        validation_instance = reseller.verify_password("Pwd@123")
        validation_ctx = ctx.verify("Pwd@123", reseller.password)
        assert validation_instance == validation_ctx

    def test_should_create_name_instance_when_set_name(self, reseller):
        reseller.set_name("Test", "Test2")
        assert isinstance(reseller._name, Name)
        assert reseller.name == "Test Test2"


# todo Criar classe de teste do model Name
