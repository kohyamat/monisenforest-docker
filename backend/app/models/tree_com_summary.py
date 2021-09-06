from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from .plot import Plot  # noqa: F401


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

    pid = Column(Integer, ForeignKey("plots.id", ondelete="CASCADE"))
    plot = relationship("Plot", back_populates="tree_com_summary")
