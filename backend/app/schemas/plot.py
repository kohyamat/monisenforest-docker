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


class PlotBase(BaseModel):
    plot_id: str
    name: str
    name_jp: str
    filename: str
    md5: str
    dtype: str
    date: Optional[str]
    size: Optional[float]


class PlotCreate(PlotBase):
    pass


class PlotUpdate(PlotBase):
    tmppath: str


class PlotInDB(PlotBase):
    id: int
    tree_com_summary: List[TreeComSummary] = []
    tree_com_turnover: List[TreeComTurnover] = []
    tree_sp_summary: List[TreeSpSummary] = []
    tree_sp_turnover: List[TreeSpTurnover] = []
    litter_each: List[LitterEach] = []
    litter_annual: List[LitterAnnual] = []
    seed_each: List[SeedEach] = []
    seed_annual: List[SeedAnnual] = []


class Plot(PlotBase):
    id: int
