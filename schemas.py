from pydantic import BaseModel


class Contest_Ranking(BaseModel):
    contestants_id: list[str]
