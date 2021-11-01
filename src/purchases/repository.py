from dataclasses import asdict
from typing import Dict, List, Optional, Protocol, runtime_checkable

from databases import Database
from sqlalchemy import Table
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import and_, select

from src.purchases.exceptions import PurchaseDoesNotExist
from src.purchases.models import Purchase, Reseller, Status


@runtime_checkable
class Repository(Protocol):
    async def add(self, purchase: Purchase) -> Purchase:
        """Method responsible for including the purchase in the db"""

    async def add_by_cpf(
        self, cpf_reseller: str, purchase: Purchase
    ) -> Purchase:
        """Method responsible for including the purchase by cpf in the db"""

    async def get(self, pk: int) -> Purchase:
        """Method responsible for seeking the purchase in the db"""

    async def update(self, pk: int, purchase: Purchase) -> bool:
        """Method responsible for editing the purchase in the db"""

    async def delete(self, pk: int) -> bool:
        """Method responsible for deleting the purchase in the db"""

    async def list_purchases(
        self, reseller_id: Optional[int] = None
    ) -> List[Purchase]:
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


class SQLAlchemyAsyncRepository:
    def __init__(self, session):
        self.session = session

    async def add(self, purchase: Purchase) -> Purchase:
        self.session.add(purchase)
        await self.session.commit()
        return purchase

    async def add_by_cpf(
        self, cpf_reseller: str, purchase: Purchase
    ) -> Purchase:
        statement = (
            select(Reseller)
            .options(selectinload(Reseller.purchases))
            .filter_by(cpf=cpf_reseller)
        )
        result = await self.session.execute(statement)

        reseller = result.scalar_one()
        reseller.add_purchase(purchase)

        await self.session.commit()
        return purchase

    async def get(self, pk: int) -> Purchase:
        statement = select(Purchase).filter_by(id=pk)
        result = await self.session.execute(statement)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise PurchaseDoesNotExist

    async def update(self, pk: int, purchase: Purchase) -> bool:
        """Method responsible for editing the purchase in the db"""

    async def delete(self, pk: int) -> bool:
        """Method responsible for deleting the purchase in the db"""

    async def list_purchases(
        self, reseller_id: Optional[int] = None
    ) -> List[Purchase]:
        """Method responsible for listing the purchases"""
