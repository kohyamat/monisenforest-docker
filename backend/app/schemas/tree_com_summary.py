from pydantic import BaseModel


class TreeComSummaryBase(BaseModel):
    year: float
    mdate: str
    nstem: float
    nsp: int
    ba: float
    b: float
    shannon: float
    richness: float
    datafile_id: int


class TreeComSummaryCreate(TreeComSummaryBase):
    pass


class TreeComSummary(TreeComSummaryBase):
    id: int

    class Config:
        orm_mode = True
