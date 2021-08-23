from typing import Dict, Protocol

import httpx
from prettyconf import config


class Client(Protocol):
    @staticmethod
    async def accrued_cashback(cpf_reseller: str) -> Dict:
        """
        Method responsible for getting the accrued caskback
        through an external client
        """


class HTTPXAsyncClient:
    @staticmethod
    async def accrued_cashback(cpf_reseller: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                config("CASHBACK_URL"),
                params={"cpf": cpf_reseller},
                headers={"token": config("CASHBACK_TOKEN")},
            )
            return response.json()
