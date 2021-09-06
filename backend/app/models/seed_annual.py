from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from .plot import Plot  # noqa: F401


class SeedAnnual(Base):
    __tablename__ = "seed_annual"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Float)
    t1 = Column(String)
    t2 = Column(String)
    inst_period = Column(Float)
    species_jp = Column(String)
    species = Column(String)
    family = Column(String)
    order = Column(String)
    wdry = Column(Float)
    number = Column(Float)
    prop_viable = Column(Float)

    pid = Column(Integer, ForeignKey("plots.id", ondelete="CASCADE"))
    plot = relationship("Plot", back_populates="seed_annual")
