from fastapi import APIRouter

from src.config import database
from src.resellers.repository import DatabaseRepository
from src.resellers.schemas import (
    ResellerIn,
    ResellerInDB,
    ResellerOut,
    VerifyPasswordIn,
    VerifyPasswordOut,
)
from src.resellers.services import ResellerService

router = APIRouter(prefix="/resellers", tags=["resellers"])
repository = DatabaseRepository(database)


@router.post("/", response_model=ResellerInDB, status_code=201)
async def create(reseller: ResellerIn):
    return await ResellerService(repository).create(reseller)


@router.get("/{pk}", response_model=ResellerOut)
async def get(pk: int):
    return await ResellerService(repository).get_by_id(pk)


@router.post("/{pk}/verify_password", response_model=VerifyPasswordOut)
async def verify_password(pk: int, password: VerifyPasswordIn):
    return await ResellerService(repository).is_valid_password(pk, password)