from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from .tree_com_summary import TreeComSummary
    from .tree_com_turnover import TreeComTurnover
    from .tree_sp_summary import TreeSpSummary
    from .tree_sp_turnover import TreeSpTurnover
    from .litter_annual import LitterAnnual
    from .litter_each import LitterEach
    from .seed_annual import SeedAnnual
    from .seed_each import SeedEach


class Plot(Base):
    __tablename__ = "plots"

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(String)
    name = Column(String)
    name_jp = Column(String)
    filename = Column(String)
    md5 = Column(String, unique=True)
    dtype = Column(String)
    date = Column(String)
    size = Column(Float)

    tree_com_summary = relationship(
        "TreeComSummary",
        back_populates="plot",
        cascade="all, delete-orphan",
    )

    tree_com_turnover = relationship(
        "TreeComTurnover",
        back_populates="plot",
        cascade="all, delete-orphan",
    )

    tree_sp_summary = relationship(
        "TreeSpSummary",
        back_populates="plot",
        cascade="all, delete-orphan",
    )

    tree_sp_turnover = relationship(
        "TreeSpTurnover",
        back_populates="plot",
        cascade="all, delete-orphan",
    )

    litter_each = relationship(
        "LitterEach",
        back_populates="plot",
        cascade="all, delete-orphan",
    )

    litter_annual = relationship(
        "LitterAnnual",
        back_populates="plot",
        cascade="all, delete-orphan",
    )

    seed_each = relationship(
        "SeedEach",
        back_populates="plot",
        cascade="all, delete-orphan",
    )

    seed_annual = relationship(
        "SeedAnnual",
        back_populates="plot",
        cascade="all, delete-orphan",
    )
