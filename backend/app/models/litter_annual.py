from typing import TYPE_CHECKING

from app.models.base import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .datafiles import Datafile  # noqa: F401


class LitterAnnual(Base):
    __tablename__ = "litter_annual"

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    t1 = Column(String)
    t2 = Column(String)
    inst_period = Column(Integer)
    n_collect = Column(Integer)
    wdry_leaf = Column(Float)
    wdry_branch = Column(Float)
    wdry_rep = Column(Float)
    wdry_all = Column(Float)

    datafile_id = Column(Integer, ForeignKey("datafiles.id", ondelete="CASCADE"))
    datafile = relationship("Datafile", back_populates="litter_annual")
