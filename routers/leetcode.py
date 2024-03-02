from fastapi import APIRouter
from .Leetcode_Contest.contest_status import contest_status
from .. import schemas
from .Database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from .Database import models
from sqlalchemy import text


router = APIRouter(
    prefix="/leetcode",
    tags=["Leetcode"]
)


@router.get("/contest/status")
async def get_contest_status():
    return contest_status()


@router.post("/contest/ranking")
async def get_contest_ranking(usernames: schemas.Contest_Ranking, db: Session = Depends(get_db)):
    sql_query = text("SELECT * FROM contests WHERE id IN :ids")
    result = db.execute(sql_query, {'ids': usernames}).fetchall()
    contestants_list = [dict(row) for row in result]
    return contestants_list
