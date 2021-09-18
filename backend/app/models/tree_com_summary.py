from typing import TYPE_CHECKING

from app.models.base import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .datafiles import Datafile  # noqa: F401


class TreeComSummary(Base):
    __tablename__ = "tree_com_summary"

    id = Column(Integer, primary_key=True)
    year = Column(Float)
    mdate = Column(String)
    nstem = Column(Float)
    nsp = Column(Integer)
    ba = Column(Float)
    b = Column(Float)
    shannon = Column(Float)
    richness = Column(Float)

    datafile_id = Column(Integer, ForeignKey("datafiles.id", ondelete="CASCADE"))
    datafile = relationship("Datafile", back_populates="tree_com_summary")
