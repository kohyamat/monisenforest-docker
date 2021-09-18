from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from .datafiles import Datafile  # noqa: F401


class SeedAnnual(Base):
    __tablename__ = "seed_annual"

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    t1 = Column(String)
    t2 = Column(String)
    inst_period = Column(Integer)
    species_jp = Column(String)
    species = Column(String)
    family = Column(String)
    order = Column(String)
    wdry = Column(Float)
    number = Column(Float)
    prop_viable = Column(Float)

    datafile_id = Column(Integer, ForeignKey("datafiles.id", ondelete="CASCADE"))
    datafile = relationship("Datafile", back_populates="seed_annual")
