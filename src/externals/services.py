from src.externals.clients import Client
from src.externals.schemas import AccruedCashbackOut


class ExternalsService:
    def __init__(self, client: Client):
        self.client = client

    async def prepare_accrued_cashback(
        self, cpf_reseller: str
    ) -> AccruedCashbackOut:
        data = await self.client.accrued_cashback(cpf_reseller)
        return AccruedCashbackOut.from_dict(data)
