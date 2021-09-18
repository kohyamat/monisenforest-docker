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
    datafile_id: int


class TreeSpSummaryCreate(TreeSpSummaryBase):
    pass


class TreeSpSummary(TreeSpSummaryBase):
    id: int

    class Config:
        orm_mode = True
