from typing import Optional

from pydantic import BaseModel


class LitterEachBase(BaseModel):
    year: float
    t1: str
    t2: str
    inst_period: float
    wdry_leaf: Optional[float]
    wdry_branch: Optional[float]
    wdry_rep: Optional[float]
    wdry_all: Optional[float]
    pid: int


class LitterEachCreate(LitterEachBase):
    pass


class LitterEachInDB(LitterEachBase):
    id: int


class LitterEach(LitterEachBase):
    id: int
