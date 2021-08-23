from fastapi import APIRouter, status

from src.config import database
from src.orm import purchases
from src.purchases.repository import DatabaseRepository
from src.purchases.schemas import PurchaseIn, PurchaseInDB, PurchaseOut
from src.purchases.services import PurchaseService

router = APIRouter(prefix="/purchases", tags=["purchases"])
repository = DatabaseRepository(database, purchases)


@router.post(
    "/", response_model=PurchaseInDB, status_code=status.HTTP_201_CREATED
)
async def create(purchase: PurchaseIn):
    return await PurchaseService(repository).prepare_create(purchase)
