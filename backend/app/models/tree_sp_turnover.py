from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from .datafiles import Datafile  # noqa: F401


class TreeSpTurnover(Base):
    __tablename__ = "tree_sp_turnover"

    id = Column(Integer, primary_key=True)
    t1 = Column(Float)
    t2 = Column(Float)
    species_jp = Column(String)
    species = Column(String)
    family = Column(String)
    order = Column(String)
    n_m = Column(Float)
    b_m = Column(Float)
    r_rel = Column(Float)
    m_rel = Column(Float)
    p_rel = Column(Float)
    l_rel = Column(Float)
    r_abs = Column(Float)
    m_abs = Column(Float)
    p_abs = Column(Float)
    l_abs = Column(Float)

    datafile_id = Column(Integer, ForeignKey("datafiles.id", ondelete="CASCADE"))
    datafile = relationship("Datafile", back_populates="tree_sp_turnover")
