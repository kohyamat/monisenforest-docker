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
    pid: int


class TreeComSummaryCreate(TreeComSummaryBase):
    pass


class TreeComSummaryInDB(TreeComSummaryBase):
    id: int


class TreeComSummary(TreeComSummaryBase):
    id: int
