from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import User
from src.db import database, get_db
from src.externals.clients import HTTPXAsyncClient
from src.externals.schemas import AccruedCashbackOut
from src.externals.services import ExternalsService
from src.orm import purchases, resellers
from src.purchases.exceptions import PurchaseDoesNotExist
from src.purchases.repository import (
    DatabaseRepository,
    SQLAlchemyAsyncRepository,
)
from src.purchases.schemas import PurchaseIn, PurchaseInDB, PurchaseOut
from src.purchases.services import PurchaseService

from ..dependencies import get_current_user

router = APIRouter(prefix="/purchases", tags=["purchases"])
repository = DatabaseRepository(database, purchases, resellers)


@router.post(
    "/", response_model=PurchaseInDB, status_code=status.HTTP_201_CREATED
)
async def create(
    purchase: PurchaseIn,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = SQLAlchemyAsyncRepository(db)
    return await PurchaseService(repository).prepare_create(purchase)


@router.get(
    "/accrued_cashback/{cpf_reseller}", response_model=AccruedCashbackOut
)
async def accrued_cashback(
    cpf_reseller: str, current_user: User = Depends(get_current_user)
):
    return await ExternalsService(HTTPXAsyncClient()).prepare_accrued_cashback(
        cpf_reseller
    )


@router.get(
    "/{pk}", response_model=PurchaseOut, status_code=status.HTTP_200_OK
)
async def get(
    pk: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = SQLAlchemyAsyncRepository(db)
    try:
        return await PurchaseService(repository).prepare_get(pk)
    except PurchaseDoesNotExist:
        raise HTTPException(status_code=404, detail="Purchase not found")


@router.put("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def update(
    pk: int,
    purchase: PurchaseIn,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = SQLAlchemyAsyncRepository(db)
    result = await PurchaseService(repository).prepare_update(pk, purchase)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Change could not be made because the purchase was not "
            "found or the status does not allow change",
        )


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    pk: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = SQLAlchemyAsyncRepository(db)
    result = await PurchaseService(repository).prepare_delete(pk)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delete could not be made because the purchase was not "
            "found or the status does not allow delete",
        )


@router.get(
    "/", response_model=List[PurchaseOut], status_code=status.HTTP_200_OK
)
async def get_items(
    reseller_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
):
    return await PurchaseService(repository).prepare_list(reseller_id)
