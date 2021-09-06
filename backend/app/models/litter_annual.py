from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from .plot import Plot  # noqa: F401


class LitterAnnual(Base):
    __tablename__ = "litter_annual"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Float)
    t1 = Column(String)
    t2 = Column(String)
    inst_period = Column(Float)
    n_collect = Column(Integer)
    wdry_leaf = Column(Float)
    wdry_branch = Column(Float)
    wdry_rep = Column(Float)
    wdry_all = Column(Float)

    pid = Column(Integer, ForeignKey("plots.id", ondelete="CASCADE"))
    plot = relationship("Plot", back_populates="litter_annual")
