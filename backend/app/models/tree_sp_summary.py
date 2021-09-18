from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from .datafiles import Datafile  # noqa: F401


class TreeSpSummary(Base):
    __tablename__ = "tree_sp_summary"

    id = Column(Integer, primary_key=True)
    year = Column(Float)
    species_jp = Column(String)
    species = Column(String)
    family = Column(String)
    order = Column(String)
    n = Column(Float)
    ba = Column(Float)
    b = Column(Float)
    n_prop = Column(Float)
    ba_prop = Column(Float)
    b_prop = Column(Float)

    datafile_id = Column(Integer, ForeignKey("datafiles.id", ondelete="CASCADE"))
    datafile = relationship("Datafile", back_populates="tree_sp_summary")
