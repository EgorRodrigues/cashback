from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    UniqueConstraint,
)

from src.purchases.models import Status

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
    UniqueConstraint("cpf"),
)


purchases = Table(
    "purchases",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("code", String(15), nullable=False),
    Column("amount", Numeric, nullable=False),
    Column("date", DateTime, nullable=False),
    Column("cashback_percent", Numeric, nullable=False),
    Column("cashback_amount", Numeric, nullable=False),
    Column("status", Enum(Status), nullable=False),
    Column("reseller_id", Integer, ForeignKey("resellers.id"), nullable=False),
)
