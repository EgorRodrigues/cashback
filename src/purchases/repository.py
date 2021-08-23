from dataclasses import asdict
from typing import Dict, Protocol

from databases import Database
from sqlalchemy import Table

from src.purchases.exceptions import PurchaseDoesNotExist
from src.purchases.models import Purchase


class Repository(Protocol):
    async def add(self, purchase: Purchase) -> Dict:
        """Method responsible for including the purchase in the db"""

    async def get(self, pk: int) -> Dict:
        """Method responsible for seeking the purchase in the db"""

    # async def update(self):
    #     """Method responsible for editing the purchase in the db"""
    #
    # async def delete(self):
    #     """Method responsible for deleting the purchase in the db"""
    #
    # async def list(self):
    #     """Method responsible for listing the purchases"""


class DatabaseRepository:
    def __init__(self, database: Database, table: Table):
        self.database = database
        self.table = table

    async def add(self, purchase: Purchase) -> Dict:
        query_reseller = "SELECT * FROM resellers WHERE cpf = :cpf"
        result = await self.database.fetch_one(
            query=query_reseller, values={"cpf": purchase.cpf_reseller}
        )
        query = self.table.insert().values(
            code=purchase.code,
            amount=purchase.amount,
            date=purchase.date,
            reseller_id=result["id"],
            cashback_percent=purchase.cashback.percent,
            cashback_amount=purchase.cashback.amount,
            status=purchase.status,
        )
        last_record_id = await self.database.execute(query)
        return {"id": last_record_id, **asdict(purchase)}

    async def get(self, pk: int) -> Dict:
        query = self.table.select().where(self.table.c.id == pk)
        result = await self.database.fetch_one(query)

        if result is None:
            raise PurchaseDoesNotExist

        purchase = Purchase(
            code=result["code"],
            amount=result["amount"],
            date=result["date"],
            cpf_reseller=result["cpf_reseller"],
            cashback_percent=result["cashback_percent"],
            cashback_amount=result["cashback_amount"],
            status=result["status"],
        )

        return {"id": result["id"], **asdict(purchase)}
