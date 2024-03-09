from pydantic import BaseModel
from typing import List, Optional


class Contest_Ranking(BaseModel):
    contestants_ids: List[str]


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


class Stock_Market_Ticker(BaseModel):
    tickers: List[str]


class Stock_Market_Ticker_Out(BaseModel):
    ticker: str
    last_quote: float

    class Config:
        from_attributes = True
