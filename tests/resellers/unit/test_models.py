import pytest
from passlib.handlers.bcrypt import bcrypt

from src.resellers.exceptions import PasswordValueError
from src.resellers.models import Name, Reseller


class TestReseller:
    def test_should_create_reseller_instance(self, reseller_model):
        assert isinstance(reseller_model, Reseller)
        assert reseller_model.cpf == "123.456.789-10"
        assert reseller_model.email == "test@test.com"

    def test_should_return_full_name_when_getting_the_attribute_name(
        self, reseller_model
    ):
        assert reseller_model.name.full == "First_Name Last_Name"

    def test_should_return_valid_bcrypt_password_when_getting_the_attribute_password(  # noqa
        self, reseller_model
    ):
        hashed_password = reseller_model.password
        str_bcrypt = bcrypt.from_string(hashed_password).to_string()
        assert hashed_password == str_bcrypt

    def test_should_create_name_instance_when_set_name(self, reseller_model):
        reseller_model.set_name("Test", "Test2")
        assert isinstance(reseller_model.name, Name)
        assert reseller_model.name.full == "Test Test2"

    def test_should_raise_password_value_error_when_there_is_no_password(self):
        with pytest.raises(PasswordValueError):
            Reseller(
                first_name="Ciclano",
                last_name="Beltrano",
                cpf="123.123.123-23",
                email="ciclano@beltrano.com",
            )

    def test_should_assign_password_when_passing_hashed_password(self):
        hashed_password = "password_hashed"
        reseller = Reseller(
            first_name="Ciclano",
            last_name="Beltrano",
            cpf="123.123.123-23",
            email="ciclano@beltrano.com",
            hashed_password=hashed_password,
        )
        assert reseller._password == hashed_password

    def test_should_get_full_name(self, reseller_model):
        assert reseller_model.full_name == "First_Name Last_Name"
