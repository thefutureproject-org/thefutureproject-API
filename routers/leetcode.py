from fastapi import APIRouter
from .Leetcode_Contest.contest_status import contest_status


router = APIRouter(
    prefix="/leetcode",
    tags=["Leetcode"]
)


@router.get("/contest/status")
async def get_linkedin_dp():
    return contest_status()
