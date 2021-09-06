from pydantic import BaseModel


class TreeSpSummaryBase(BaseModel):
    year: float
    species_jp: str
    species: str
    family: str
    order: str
    n: float
    ba: float
    b: float
    n_prop: float
    ba_prop: float
    b_prop: float
    pid: int


class TreeSpSummaryCreate(TreeSpSummaryBase):
    pass


class TreeSpSummaryInDB(TreeSpSummaryBase):
    id: int


class TreeSpSummary(TreeSpSummaryBase):
    id: int
