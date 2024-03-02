from pydantic import BaseModel
from typing import List


class Contest_Ranking(BaseModel):
    contestants_id: List[str]


class Contest_Ranking_Out(BaseModel):
    username: str
    rank: int
    finish_time: str
    A_st: str
    A_flc: int
    B_st: str
    B_flc: int
    C_st: str
    C_flc: int
    D_st: str
    D_flc: int

    class Config:
        from_attributes = True
