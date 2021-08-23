from src.resellers.repository import Repository
from src.resellers.schemas import ResellerIn, ResellerInDB, ResellerOut


class ResellerService:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def prepare_create(self, reseller: ResellerIn) -> ResellerInDB:
        result = await self.repository.add(reseller.to_model())
        return ResellerInDB.from_dict(result)

    async def prepare_get(self, pk: int) -> ResellerOut:
        result = await self.repository.get(pk)
        return ResellerOut.from_dict(result)
