from .database import Base
from sqlalchemy import Column, Integer, String


class Contest(Base):
    __tablename__ = 'contests'

    username = Column(String, primar_key=True, nullable=False)
    rank = Column(Integer, nullable=False)
    finish_time = Column(String, nullable=False)

    A_st = Column(String)
    A_flc = Column(Integer)

    B_st = Column(String)
    B_flc = Column(Integer)

    C_st = Column(String)
    C_flc = Column(Integer)

    D_st = Column(String)
    D_flc = Column(Integer)
