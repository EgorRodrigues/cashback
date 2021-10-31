from typing import Protocol, runtime_checkable

from sqlalchemy import select

from src.resellers.models import Reseller


@runtime_checkable
class Repository(Protocol):
    async def add(self, reseller: Reseller) -> Reseller:
        """Method responsible for including the reseller in the db"""

    async def get(self, pk: int) -> Reseller:
        """Method responsible for getting the reseller in the db"""


class SQLAlchemyAsyncRepository:
    def __init__(self, session):
        self.session = session

    async def add(self, reseller: Reseller) -> Reseller:
        self.session.add(reseller)
        await self.session.commit()
        return reseller

    async def get(self, pk: int) -> Reseller:
        statement = select(Reseller).filter_by(id=pk)
        result = await self.session.execute(statement)
        return result.scalar_one()
