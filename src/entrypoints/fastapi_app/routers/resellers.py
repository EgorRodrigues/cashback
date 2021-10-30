from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import User
from src.db import database, get_db
from src.orm import resellers
from src.resellers.exceptions import ResellerDoesNotExist
from src.resellers.repository import (
    DatabaseRepository,
    SQLAlchemyAsyncRepository,
)
from src.resellers.schemas import ResellerIn, ResellerInDB, ResellerOut
from src.resellers.services import ResellerService

from ..dependencies import get_current_user

router = APIRouter(prefix="/resellers", tags=["resellers"])
repository = DatabaseRepository(database, resellers)


@router.post(
    "/", response_model=ResellerInDB, status_code=status.HTTP_201_CREATED
)
async def create(reseller: ResellerIn, db: AsyncSession = Depends(get_db)):
    repository = SQLAlchemyAsyncRepository(db)
    return await ResellerService(repository).prepare_create(reseller)


@router.get("/{pk}", response_model=ResellerOut)
async def get(pk: int, current_user: User = Depends(get_current_user)):
    try:
        return await ResellerService(repository).prepare_get(pk)
    except ResellerDoesNotExist:
        raise HTTPException(status_code=404, detail="Reseller not found")
