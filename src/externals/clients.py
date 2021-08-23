import httpx
from prettyconf import config


class CashbackClient:
    @staticmethod
    async def accrued(cpf_reseller) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                config("CASHBACK_URL"),
                params={"cpf": cpf_reseller},
                headers={"token": config("CASHBACK_TOKEN")},
            )
            return response
