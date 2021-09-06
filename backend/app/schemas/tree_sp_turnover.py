from pydantic import BaseModel


class TreeSpTurnoverBase(BaseModel):
    t1: float
    t2: float
    species_jp: str
    species: str
    family: str
    order: str
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


class TreeSpTurnoverCreate(TreeSpTurnoverBase):
    pass


class TreeSpTurnoverInDB(TreeSpTurnoverBase):
    id: int


class TreeSpTurnover(TreeSpTurnoverBase):
    id: int
