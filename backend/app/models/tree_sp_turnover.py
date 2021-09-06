from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from .plot import Plot  # noqa: F401


class TreeSpTurnover(Base):
    __tablename__ = "tree_sp_turnover"

    id = Column(Integer, primary_key=True, index=True)
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

    pid = Column(Integer, ForeignKey("plots.id", ondelete="CASCADE"))
    plot = relationship("Plot", back_populates="tree_sp_turnover")
