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
        return ResellerOut(
            id=obj.id,
            cpf=obj.cpf,
            email=obj.email,
            name=obj.name.full,
        )


class ResellerInDB(ResellerBase):
    id: int
    first_name: str
    last_name: str
    hashed_password: str

    @staticmethod
    def from_dict(obj) -> "ResellerInDB":
        return ResellerInDB(
            id=obj.id,
            cpf=obj.cpf,
            email=obj.email,
            first_name=obj.first_name,
            last_name=obj.last_name,
            hashed_password=obj._password,
        )
