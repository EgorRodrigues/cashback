from dataclasses import asdict
from typing import Dict, Protocol

from src.resellers.models import Reseller
from src.resellers.schemas import resellers


class Repository(Protocol):
    def add(self, reseller: Reseller) -> Dict:
        """Method responsible for including the reseller in the db"""


class DatabaseRepository:
    def __init__(self, database):
        self.database = database

    async def add(self, reseller: Reseller) -> Dict:
        query = resellers.insert().values(
            first_name=reseller.name.first,
            last_name=reseller.name.last,
            cpf=reseller.cpf,
            email=reseller.email,
            password=reseller.password,
        )
        last_record_id = await self.database.execute(query)
        return {**asdict(reseller), "id": last_record_id}
