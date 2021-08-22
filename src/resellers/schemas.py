from pydantic import BaseModel
from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper

from src.resellers.models import Reseller as ResellerModel

metadata = MetaData()


resellers = Table(
    "resellers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String(50), nullable=False),
    Column("last_name", String(50), nullable=False),
    Column("cpf", String(14), nullable=False),
    Column("email", String(150), nullable=False),
    Column("password", String(100), nullable=False),
)


def start_mappers():
    mapper(
        ResellerModel,
        resellers,
    )


class ResellerBase(BaseModel):
    cpf: str
    email: str


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


class ResellerInDB(ResellerBase):
    id: int
    first_name: str
    last_name: str
    hashed_password: str


class VerifyPasswordOut(BaseModel):
    is_valid: bool


class VerifyPasswordIn(BaseModel):
    plain_password: str
