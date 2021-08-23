from typing import Dict

from src.purchases.repository import Repository
from src.purchases.schemas import PurchaseIn, PurchaseInDB


class PurchaseService:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def prepare_create(self, purchase: PurchaseIn) -> PurchaseInDB:
        print("--->>>", purchase.to_model())
        result = await self.repository.add(purchase.to_model())
        return PurchaseInDB.from_dict(result)
