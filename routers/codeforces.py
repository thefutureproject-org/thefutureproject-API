from fastapi import APIRouter, status
import schemas
from fastapi import HTTPException, status
from config import settings
import requests
import asyncio


router = APIRouter(
    prefix="/codeforces",
    tags=["Codeforces API"]
)


async def profile_info(username: str):
    url = "https://codeforces.com/api/user.info"
    params = {
        "handles": username,
        "checkHistoricHandles": "false"
    }

    response = requests.get(
        url, params=params, proxies=settings.PROXIES)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch user data")

    data = response.json()["result"]
    return data[0]


async def rating_info(username: str):
    url = "https://codeforces.com/api/user.rating"
    params = {
        "handle": username
    }

    response = requests.get(
        url, params=params, proxies=settings.PROXIES)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch user data")

    data = response.json()["result"]
    return data


@router.post("/user", status_code=status.HTTP_201_CREATED, summary="Get user information")
async def get_user(profile: schemas.Codeforces_profile_In):
    profile_task = profile_info(profile.username)
    rating_task = rating_info(profile.username)
    profile_data, rating_data = await asyncio.gather(profile_task, rating_task)
    profile_data["number_of_contests"] = len(rating_data)
    return profile_data
