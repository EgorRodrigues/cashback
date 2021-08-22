from typing import Dict

from fastapi import HTTPException

from src.resellers.exceptions import ResellerDoesNotExist
from src.resellers.models import Reseller as ResellerModel
from src.resellers.repository import Repository
from src.resellers.schemas import (
    ResellerIn,
    ResellerInDB,
    ResellerOut,
    VerifyPasswordIn,
    VerifyPasswordOut,
)


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

    async def prepare_verify_password(
        self, pk: int, verify_password: VerifyPasswordIn
    ) -> VerifyPasswordOut:
        result = await self._get_by_id(pk)
        is_valid = ResellerModel.verify_password(
            verify_password.plain_password, result["_password"]
        )
        return VerifyPasswordOut(is_valid=is_valid)
