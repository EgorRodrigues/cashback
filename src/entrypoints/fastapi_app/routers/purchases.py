from fastapi import APIRouter, status

from src.config import database
from src.externals.clients import HTTPXAsyncClient
from src.externals.schemas import AccruedCashbackOut
from src.externals.services import ExternalsService
from src.orm import purchases, resellers
from src.purchases.repository import DatabaseRepository
from src.purchases.schemas import PurchaseIn, PurchaseInDB, PurchaseOut
from src.purchases.services import PurchaseService

router = APIRouter(prefix="/purchases", tags=["purchases"])
repository = DatabaseRepository(database, purchases, resellers)


@router.post(
    "/", response_model=PurchaseInDB, status_code=status.HTTP_201_CREATED
)
async def create(purchase: PurchaseIn):
    return await PurchaseService(repository).prepare_create(purchase)


@router.get(
    "/accrued_cashback/{cpf_reseller}", response_model=AccruedCashbackOut
)
async def accrued_cashback(cpf_reseller: str):
    return await ExternalsService(HTTPXAsyncClient).prepare_accrued_cashback(
        cpf_reseller
    )


@router.get("/", response_model=PurchaseOut, status_code=status.HTTP_200_OK)
async def get(pk: int):
    return await PurchaseService(repository).prepare_get(pk)
