from dataclasses import asdict
from typing import Dict, Protocol, runtime_checkable

from databases import Database
from sqlalchemy import Table

from src.resellers.exceptions import ResellerDoesNotExist
from src.resellers.models import Reseller


@runtime_checkable
class Repository(Protocol):
    async def add(self, reseller: Reseller) -> Dict:
        """Method responsible for including the reseller in the db"""

    async def get(self, pk: int) -> Dict:
        """Method responsible for getting the reseller in the db"""


class DatabaseRepository:
    def __init__(self, database: Database, table: Table):
        self.database = database
        self.table = table

    async def add(self, reseller: Reseller) -> Dict:
        query = self.table.insert().values(
            first_name=reseller.name.first,
            last_name=reseller.name.last,
            cpf=reseller.cpf,
            email=reseller.email,
            password=reseller.password,
        )
        last_record_id = await self.database.execute(query)
        return {"id": last_record_id, **asdict(reseller)}

    async def get(self, pk: int) -> Dict:
        query = self.table.select().where(self.table.c.id == pk)
        result = await self.database.fetch_one(query)

        if result is None:
            raise ResellerDoesNotExist

        reseller = Reseller(
            first_name=result["first_name"],
            last_name=result["first_name"],
            cpf=result["cpf"],
            email=result["email"],
            hashed_password=result["password"],
        )

        return {"id": result["id"], **asdict(reseller)}
