from fastapi import APIRouter

router = APIRouter(
    prefix="/resellers",
    tags=["resellers"]
)


@router.post("/")
def create_reseller():
    ...
