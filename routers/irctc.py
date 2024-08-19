from fastapi import APIRouter
from .IRCTC.pnr_status import get_pnr_status

router = APIRouter(
    prefix="/irctc",
    tags=["IRCTC"]
)

@router.get("/pnr/{pnr}")
async def pnr_status(pnr: str):
    return get_pnr_status(pnr)