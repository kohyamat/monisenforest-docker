from pydantic import BaseModel


class TreeComTurnoverBase(BaseModel):
    t1: float
    t2: float
    n_m: int
    b_m: float
    r_rel: float
    m_rel: float
    p_rel: float
    l_rel: float
    r_abs: float
    m_abs: float
    p_abs: float
    l_abs: float
    datafile_id: int


class TreeComTurnoverCreate(TreeComTurnoverBase):
    pass


class TreeComTurnover(TreeComTurnoverBase):
    id: int

    class Config:
        orm_mode = True
