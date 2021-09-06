from typing import Optional

from pydantic import BaseModel


class LitterAnnualBase(BaseModel):
    year: float
    n_collect: int
    t1: str
    t2: str
    inst_period: float
    wdry_leaf: Optional[float]
    wdry_branch: Optional[float]
    wdry_rep: Optional[float]
    wdry_all: Optional[float]
    pid: int


class LitterAnnualCreate(LitterAnnualBase):
    pass


class LitterAnnualInDB(LitterAnnualBase):
    id: int


class LitterAnnual(LitterAnnualBase):
    id: int
