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
    pid: int


class TreeComTurnoverCreate(TreeComTurnoverBase):
    pass


class TreeComTurnoverInDB(TreeComTurnoverBase):
    id: int


class TreeComTurnover(TreeComTurnoverBase):
    id: int
