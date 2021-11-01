from typing import List, Optional

from src.purchases.repository import Repository
from src.purchases.schemas import PurchaseIn, PurchaseInDB, PurchaseOut


class PurchaseService:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def prepare_create(self, purchase: PurchaseIn) -> PurchaseInDB:
        result = await self.repository.add_by_cpf(
            purchase.cpf_reseller, purchase.to_model()
        )
        return PurchaseInDB.from_dict(result)

    async def prepare_get(self, pk: int) -> PurchaseOut:
        result = await self.repository.get(pk)
        return PurchaseOut.from_dict(result)

    async def prepare_update(self, pk: int, purchase: PurchaseIn) -> bool:
        result = await self.repository.update(pk, purchase.to_model())
        return result

    async def prepare_delete(self, pk: int) -> bool:
        result = await self.repository.delete(pk)
        return result

    async def prepare_list(self, reseller_id: Optional[int] = None) -> List:
        result = await self.repository.list_purchases(reseller_id)
        return result
