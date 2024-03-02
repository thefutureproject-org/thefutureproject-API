from pydantic import BaseModel
from typing import List, Optional


class Contest_Ranking(BaseModel):
    contestants_id: List[str]


class Contest_Ranking_Out(BaseModel):
    username: str
    rank: int
    finish_time: str
    A_st: Optional[str]
    A_flc: Optional[int]
    B_st: Optional[str]
    B_flc: Optional[int]
    C_st: Optional[str]
    C_flc: Optional[int]
    D_st: Optional[str]
    D_flc: Optional[int]

    class Config:
        from_attributes = True
