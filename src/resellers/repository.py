from typing import Protocol

from src.resellers.models import Reseller
from src.resellers.schemas import resellers, Reseller as ResellerSchema


class Repository(Protocol):
    def add(self, reseller: Reseller) -> int:
        """Method responsible for including the reseller in the db"""

    def get(self, pk: int) -> Reseller:
        """Method responsible for getting the reseller in the db"""


class DatabaseRepository:
    def __init__(self, database):
        self.database = database

    async def add(self, reseller: Reseller) -> int:
        query = resellers.insert().values(
            first_name=reseller.name.first,
            last_name=reseller.name.last,
            cpf=reseller.cpf,
            email=reseller.email,
            password=reseller.password,
        )
        last_record_id = await self.database.execute(query)
        return last_record_id

    async def get(self, pk: int) -> ResellerSchema:
        query = resellers.select().where(resellers.c.id == pk)
        result = await self.database.fetch_one(query)

        name = f"{result['first_name']} {result['last_name']}"
        reseller = ResellerSchema(
            id=result['id'],
            name=name,
            cpf=result['cpf'],
            email=result['email']
        )
        return reseller
