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


class ResellerIn(BaseModel):
    first_name: str
    last_name: str
    cpf: str
    email: str
    password: str


class ResellerCreated(BaseModel):
    id: int


class Reseller(BaseModel):
    id: int
    name: str
    cpf: str
    email: str
