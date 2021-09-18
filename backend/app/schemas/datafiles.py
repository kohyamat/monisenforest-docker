from typing import List, Optional

from app.schemas.litter_annual import LitterAnnual
from app.schemas.litter_each import LitterEach
from app.schemas.seed_annual import SeedAnnual
from app.schemas.seed_each import SeedEach
from app.schemas.tree_com_summary import TreeComSummary
from app.schemas.tree_com_turnover import TreeComTurnover
from app.schemas.tree_sp_summary import TreeSpSummary
from app.schemas.tree_sp_turnover import TreeSpTurnover
from pydantic import BaseModel


class DatafileBase(BaseModel):
    plot_id: str
    name: str
    name_jp: str
    filename: str
    md5: str
    dtype: str
    date: Optional[str]
    size: Optional[float]


class DatafileCreate(DatafileBase):
    pass


class DatafileUpdate(DatafileBase):
    tmppath: str


class Datafile(DatafileBase):
    id: int

    class Config:
        orm_mode = True
