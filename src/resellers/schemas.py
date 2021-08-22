from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper
from pydantic import dataclasses

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


Reseller = dataclasses.dataclass(ResellerModel)
