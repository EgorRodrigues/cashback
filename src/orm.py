from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import composite, registry, relationship, synonym

from src.purchases.models import Purchase, Status
from src.resellers.models import Name, Reseller

mapper_registry = registry()


resellers = Table(
    "resellers",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String(50), nullable=False),
    Column("last_name", String(50), nullable=False),
    Column("cpf", String(14), nullable=False),
    Column("email", String(150), nullable=False),
    Column("password", String(100), nullable=False),
    UniqueConstraint("cpf"),
)


purchases = Table(
    "purchases",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("code", String(15), nullable=False),
    Column("amount", Numeric, nullable=False),
    Column("date", DateTime, nullable=False),
    Column("cashback_percent", Numeric, nullable=False),
    Column("cashback_amount", Numeric, nullable=False),
    Column("status", Enum(Status), nullable=False),
    Column("reseller_id", Integer, ForeignKey("resellers.id"), nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(
        Reseller,
        resellers,
        properties={
            "name": composite(
                Name, resellers.c.first_name, resellers.c.last_name
            ),
            "password": synonym(
                "_password", map_column=True, descriptor=Reseller.password
            ),
            "purchases": relationship(
                Purchase, backref="resellers", order_by=purchases.c.id
            ),
        },
    )
    mapper_registry.map_imperatively(Purchase, purchases)
