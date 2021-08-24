from dataclasses import asdict
from typing import Dict, List, Optional, Protocol, runtime_checkable

from databases import Database
from sqlalchemy import Table
from sqlalchemy.sql import and_, select

from src.purchases.exceptions import PurchaseDoesNotExist
from src.purchases.models import Purchase, Status


@runtime_checkable
class Repository(Protocol):
    async def add(self, purchase: Purchase) -> Dict:
        """Method responsible for including the purchase in the db"""

    async def get(self, pk: int) -> Dict:
        """Method responsible for seeking the purchase in the db"""

    async def update(self, pk: int, purchase: Purchase) -> bool:
        """Method responsible for editing the purchase in the db"""

    async def delete(self, pk: int) -> bool:
        """Method responsible for deleting the purchase in the db"""

    async def list_purchases(self, reseller_id: Optional[int] = None) -> List:
        """Method responsible for listing the purchases"""


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
        reseller_id = (
            select([self.resellers_table.c.id])
            .where(self.resellers_table.c.cpf == purchase.cpf_reseller)
            .limit(1)
        )
        query = self.purchases_table.insert().values(
            code=purchase.code,
            amount=purchase.amount,
            date=purchase.date,
            reseller_id=reseller_id,
            cashback_percent=purchase.cashback.percent,
            cashback_amount=purchase.cashback.amount,
            status=purchase.status,
        )
        last_record_id = await self.database.execute(query)
        return {"id": last_record_id, **asdict(purchase)}

    async def get(self, pk: int) -> Dict:
        query = (
            self.purchases_table.join(self.resellers_table)
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

    async def update(self, pk: int, purchase: Purchase) -> bool:
        query = (
            self.purchases_table.update()
            .where(
                and_(
                    self.purchases_table.c.id == pk,
                    self.purchases_table.c.status == Status.IN_VALIDATION,
                )
            )
            .values(
                code=purchase.code,
                amount=purchase.amount,
                date=purchase.date,
                cashback_percent=purchase.cashback.percent,
                cashback_amount=purchase.cashback.amount,
                status=purchase.status,
            )
        )
        result = await self.database.execute(query=query)
        return bool(result)

    async def delete(self, pk: int) -> bool:
        query = self.purchases_table.delete().where(
            and_(
                self.purchases_table.c.id == pk,
                self.purchases_table.c.status == Status.IN_VALIDATION,
            )
        )
        result = await self.database.execute(query=query)
        return bool(result)

    async def list_purchases(self, reseller_id: Optional[int] = None) -> List:
        query = select(
            [
                self.purchases_table,
                self.resellers_table.c.cpf.label("cpf_reseller"),
            ]
        ).select_from(self.purchases_table.join(self.resellers_table))
        if reseller_id is not None:
            query = query.where(self.resellers_table.c.id == reseller_id)
        rows = await self.database.fetch_all(query=query)
        result = [dict(row) for row in rows]
        return result
