from typing import Dict, Protocol

from databases import Database
from sqlalchemy import Table

from src.auth.exceptions import UserDoesNotExist


class Repository(Protocol):
    async def get_by_email(self, email: str) -> Dict:
        """Method responsible for getting the reseller by email"""


class DatabaseRepository:
    def __init__(self, database: Database, table: Table):
        self.database = database
        self.table = table

    async def get_by_email(self, email: str) -> Dict:
        query = self.table.select().where(self.table.c.email == email)
        result = await self.database.fetch_one(query)

        if result is None:
            raise UserDoesNotExist

        return dict(result)
