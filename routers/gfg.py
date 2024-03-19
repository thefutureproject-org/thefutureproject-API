from fastapi import APIRouter
import schemas
from .GFG_Modules import problem_info

router = APIRouter(
    prefix="/gfg",
    tags=["GeeksForGeeks"]
)


@router.post("/problem/info", status_code=200, summary="Get problem details from GFG")
async def get_problem_info(problem: schemas.GFG_Problem_In):
    data = problem_info.get_problem_data(problem.title_slug)
    return data
