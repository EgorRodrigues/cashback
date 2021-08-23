from pydantic import BaseModel, EmailStr

from src.resellers.models import Reseller as ResellerModel


class ResellerBase(BaseModel):
    cpf: str
    email: EmailStr


class ResellerIn(ResellerBase):
    first_name: str
    last_name: str
    password: str

    def to_model(self) -> ResellerModel:
        return ResellerModel(
            first_name=self.first_name,
            last_name=self.last_name,
            cpf=self.cpf,
            email=self.email,
            plain_password=self.password,
        )


class ResellerOut(ResellerBase):
    id: int
    name: str

    @staticmethod
    def from_dict(obj) -> "ResellerOut":
        name = f'{obj["name"]["first"]} {obj["name"]["last"]}'
        return ResellerOut(
            id=obj["id"],
            cpf=obj["cpf"],
            email=obj["email"],
            name=name,
        )


class ResellerInDB(ResellerBase):
    id: int
    first_name: str
    last_name: str
    hashed_password: str

    @staticmethod
    def from_dict(obj) -> "ResellerInDB":
        return ResellerInDB(
            id=obj["id"],
            cpf=obj["cpf"],
            email=obj["email"],
            first_name=obj["name"]["first"],
            last_name=obj["name"]["last"],
            hashed_password=obj["_password"],
        )


class VerifyPasswordOut(BaseModel):
    is_valid: bool


class VerifyPasswordIn(BaseModel):
    plain_password: str
