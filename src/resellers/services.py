from typing import Dict

from src.config import database
from src.resellers.models import Reseller as ResellerModel
from src.resellers.repository import DatabaseRepository
from src.resellers.schemas import Reseller, ResellerIn


class ResellerService:
    @staticmethod
    async def create(reseller: ResellerIn) -> Dict:
        repository = DatabaseRepository(database)
        model = ResellerModel(
            first_name=reseller.first_name,
            last_name=reseller.last_name,
            cpf=reseller.cpf,
            email=reseller.email,
            plain_password=reseller.password,
        )
        last_id = await repository.add(model)
        response = {"id": last_id}
        return response

    @staticmethod
    async def get_by_id(pk) -> Reseller:
        repository = DatabaseRepository(database)
        return await repository.get(pk)
