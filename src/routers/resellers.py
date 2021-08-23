from fastapi import APIRouter, status

from src.config import database
from src.orm import resellers
from src.resellers.repository import DatabaseRepository
from src.resellers.schemas import ResellerIn, ResellerInDB, ResellerOut
from src.resellers.services import ResellerService

router = APIRouter(prefix="/resellers", tags=["resellers"])
repository = DatabaseRepository(database, resellers)


@router.post(
    "/", response_model=ResellerInDB, status_code=status.HTTP_201_CREATED
)
async def create(reseller: ResellerIn):
    return await ResellerService(repository).prepare_create(reseller)


@router.get("/{pk}", response_model=ResellerOut)
async def get(pk: int):
    return await ResellerService(repository).prepare_get(pk)
