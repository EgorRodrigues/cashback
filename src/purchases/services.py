from typing import Dict

from fastapi import HTTPException

from src.purchases.exceptions import PurchaseDoesNotExist
from src.purchases.repository import Repository
from src.purchases.schemas import PurchaseIn, PurchaseInDB, PurchaseOut


class PurchaseService:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def _get_by_id(self, pk: int) -> Dict:
        try:
            return await self.repository.get(pk)
        except PurchaseDoesNotExist:
            raise HTTPException(status_code=404, detail="Purchase not found")

    async def prepare_create(self, purchase: PurchaseIn) -> PurchaseInDB:
        result = await self.repository.add(purchase.to_model())
        return PurchaseInDB.from_dict(result)

    async def prepare_get(self, pk: int) -> PurchaseOut:
        result = await self._get_by_id(pk)
        return PurchaseOut.from_dict(result)
