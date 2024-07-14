from fastapi import APIRouter, Header, HTTPException
from .Leetcode_Contest.contest_status import contest_status
from .Leetcode_Contest.contest_info import contest_info
from .Leetcode_Contest.leetcode_problem_info import get_problem_info
from .Leetcode_Contest.profile_scrape import user_info
from .Leetcode_Contest.contest_analysis import get_all_submissions
import schemas
from .Database.database import get_db
from .Database.mongodb import get_mdb
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.orm import Session
from fastapi import Depends
from .Database import models
from typing import List
from sqlalchemy import func
import random
from fastapi.responses import JSONResponse
import httpx
from config import settings


router = APIRouter(
    prefix="/leetcode",
    tags=["Leetcode"]
)


@router.get("/contest/status")
async def get_contest_status():
    return contest_status()


@router.post("/contest/ranking", response_model=List[schemas.Contest_Ranking_Out])
async def get_contest_ranking(usernames: schemas.Contest_Ranking, origin: str = Header(None, include_in_schema=False), db: Session = Depends(get_db)):
    if (origin == "chrome-extension://mcfpimbkecfbccgdamgejenmljjcamce"):
        contests = db.query(models.Contest).filter(
            func.lower(models.Contest.username).in_(
                [username.lower() for username in usernames.contestants_ids]
            )
        ).all()
        return contests
    else:
        user_data = [
            {
                "username": username,
                "rank": random.randint(1, 25000),
                "finish_time": f"{random.randint(0, 1)}:{random.randint(0, 30)}:{random.randint(0, 60)}",
                "A_st": f"{random.randint(0, 1)}:{random.randint(0, 30)}:{random.randint(0, 60)}",
                "A_flc": random.randint(0, 2),
                "B_st": f"{random.randint(0, 1)}:{random.randint(0, 30)}:{random.randint(0, 60)}",
                "B_flc": random.randint(0, 4),
                "C_st": f"{random.randint(0, 1)}:{random.randint(0, 30)}:{random.randint(0, 60)}",
                "C_flc": random.randint(0, 6),
                "D_st": f"{random.randint(0, 1)}:{random.randint(0, 30)}:{random.randint(0, 60)}",
                "D_flc": random.randint(0, 8)
            } for username in usernames.contestants_ids
        ]
        return user_data


@router.post("/contest/info/hidden", response_model=schemas.Contest_Info_Out, summary="Contest Info Hidden API")
async def get_contest_info(contest_name: schemas.Contest_Info_In):
    return contest_info(contest_name.contest_name)


@router.get("/contest/info/{contest_name}")
async def get_contest_info(contest_name: str, client: AsyncIOMotorClient = Depends(get_mdb)):
    db = client.Contest
    collection = db.Contest_info
    contest_data = await collection.find_one({contest_name: {"$exists": True}})
    if contest_data:
        return contest_data[contest_name]
    else:
        raise HTTPException(status_code=404, detail="Contest not found")


@router.post("/problem/info", response_model=schemas.Problem_Info_Out)
async def problem_info(problem: schemas.Problem_Info_In):
    return get_problem_info(problem.title_slug)


@router.post("/profile/info")
async def get_profile_info(username: schemas.Leetcode_Username_In):
    return user_info(username.username)


@router.post("/contest/analysis/hidden", summary="Contest Analysis Hidden API")
async def get_contest_analysis(contest: schemas.Contest_Analysis_In):
    return await get_all_submissions(contest.contest_name)


@router.get("/contest/analysis/{contest_name}", response_model=schemas.ContestData)
async def get_contest_data(contest_name: str, client: AsyncIOMotorClient = Depends(get_mdb)):
    db = client.Contest

    if contest_name.startswith("weekly"):
        collection = db.Weekly
        contest_data = await collection.find_one({contest_name: {"$exists": True}})
        if contest_data:
            return {"contest_name": contest_name, "data": contest_data[contest_name]}
    elif contest_name.startswith("biweekly"):
        collection = db.Biweekly
        contest_data = await collection.find_one({contest_name: {"$exists": True}})
        if contest_data:
            return {"contest_name": contest_name, "data": contest_data[contest_name]}

    raise HTTPException(status_code=404, detail="Contest not found")


@router.get("/get-prediction/{username}/{weekly_contest}")
async def get_prediction(weekly_contest: str = "weekly-contest-404", username: str = "Chandrachur"):
    api_url = f"https://lccn.lbao.site/api/v1/contest-records/user?contest_name={weekly_contest}&username={username}&archived=false"

    async with httpx.AsyncClient(proxy=settings.PROXY_URL) as client:
        response = await client.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return JSONResponse(content=data)
    else:
        raise HTTPException(
            status_code=500, detail="Failed to fetch data from the API")
