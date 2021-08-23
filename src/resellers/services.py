from typing import Dict

from fastapi import HTTPException

from src.resellers.exceptions import ResellerDoesNotExist
from src.resellers.repository import Repository
from src.resellers.schemas import ResellerIn, ResellerInDB, ResellerOut


class ResellerService:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def _get_by_id(self, pk: int) -> Dict:
        try:
            return await self.repository.get(pk)
        except ResellerDoesNotExist:
            raise HTTPException(status_code=404, detail="Reseller not found")

    async def prepare_create(self, reseller: ResellerIn) -> ResellerInDB:
        result = await self.repository.add(reseller.to_model())
        return ResellerInDB.from_dict(result)

    async def prepare_get(self, pk: int) -> ResellerOut:
        result = await self._get_by_id(pk)
        return ResellerOut.from_dict(result)
