from fastapi import APIRouter

from src.resellers.schemas import Reseller, ResellerCreated, ResellerIn
from src.resellers.services import ResellerService

router = APIRouter(prefix="/resellers", tags=["resellers"])


@router.post("/", response_model=ResellerCreated)
async def create(reseller: ResellerIn):
    return await ResellerService.create(reseller)


@router.get("/{pk}", response_model=Reseller)
async def get(pk: int):
    return await ResellerService.get_by_id(pk)
