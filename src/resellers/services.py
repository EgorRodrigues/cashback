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

    async def create(self, reseller: ResellerIn) -> ResellerInDB:
        return await self.repository.add(reseller.to_model())

    async def get_by_id(self, pk: int) -> ResellerOut:
        try:
            result = await self.repository.get(pk)
            return ResellerOut(
                id=result.id,
                name=f"{result.first_name} {result.last_name}",
                cpf=result.cpf,
                email=result.email,
            )
        except ResellerDoesNotExist:
            raise HTTPException(status_code=404, detail="Reseller not found")

    async def is_valid_password(
        self, pk: int, verify_password: VerifyPasswordIn
    ) -> VerifyPasswordOut:
        try:
            result = await self.repository.get(pk)
            is_valid = ResellerModel.verify_password(
                verify_password.plain_password, result.hashed_password
            )
            return VerifyPasswordOut(is_valid=is_valid)
        except ResellerDoesNotExist:
            raise HTTPException(status_code=404, detail="Reseller not found")
