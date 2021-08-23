from dataclasses import asdict
from typing import Dict, Protocol

from databases import Database
from sqlalchemy import Table

from src.purchases.exceptions import PurchaseDoesNotExist
from src.purchases.models import Cashback, Purchase, Status


class Repository(Protocol):
    async def add(self, purchase: Purchase) -> Dict:
        """Method responsible for including the purchase in the db"""

    async def get(self, reseller_table: Table, pk: int) -> Dict:
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
    def __init__(
        self,
        database: Database,
        purchases_table: Table,
        resellers_table: Table,
    ):
        self.database = database
        self.purchases_table = purchases_table
        self.resellers_table = resellers_table

    async def add(self, purchase: Purchase) -> Dict:
        query_reseller = "SELECT * FROM resellers WHERE cpf = :cpf"
        result = await self.database.fetch_one(
            query=query_reseller, values={"cpf": purchase.cpf_reseller}
        )
        query = self.purchases_table.insert().values(
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
        query = (
            self.purchases_table
            .join(self.resellers_table)
            .select()
            .where(self.purchases_table.c.id == pk)
        )
        row = await self.database.fetch_one(query=query)

        if row is None:
            raise PurchaseDoesNotExist

        purchase = Purchase(
            code=row["code"],
            amount=row["amount"],
            date=row["date"],
            cpf_reseller=row["cpf"],
            status=row["status"],
        )

        return {"id": row[self.purchases_table.c.id], **asdict(purchase)}
