from fastapi import APIRouter, status

router = APIRouter(
    prefix="/codeforces",
    tags=["Codeforces API"]
)


@router.post("/user", status_code=status.HTTP_201_CREATED, summary="Get user information")
async def get_user():
    return {"message": "User information fetched successfully"}
