from typing import Protocol

from src.resellers.exceptions import ResellerDoesNotExist
from src.resellers.models import Reseller
from src.resellers.schemas import ResellerInDB, resellers


class Repository(Protocol):
    async def add(self, reseller: Reseller) -> ResellerInDB:
        """Method responsible for including the reseller in the db"""

    async def get(self, pk: int) -> ResellerInDB:
        """Method responsible for getting the reseller in the db"""


class DatabaseRepository:
    def __init__(self, database):
        self.database = database

    async def add(self, reseller: Reseller) -> ResellerInDB:
        query = resellers.insert().values(
            first_name=reseller.name.first,
            last_name=reseller.name.last,
            cpf=reseller.cpf,
            email=reseller.email,
            password=reseller.password,
        )
        last_record_id = await self.database.execute(query)
        response = ResellerInDB(
            id=last_record_id,
            first_name=reseller.name.first,
            last_name=reseller.name.last,
            cpf=reseller.cpf,
            email=reseller.email,
            hashed_password=reseller.password,
        )
        return response

    async def get(self, pk: int) -> ResellerInDB:
        query = resellers.select().where(resellers.c.id == pk)
        result = await self.database.fetch_one(query)

        if result is None:
            raise ResellerDoesNotExist

        reseller = ResellerInDB(
            id=result["id"],
            first_name=result["first_name"],
            last_name=result["last_name"],
            cpf=result["cpf"],
            email=result["email"],
            hashed_password=result["password"],
        )
        return reseller
