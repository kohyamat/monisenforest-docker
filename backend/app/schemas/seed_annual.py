from typing import Optional

from pydantic import BaseModel


class SeedAnnualBase(BaseModel):
    year: float
    t1: str
    t2: str
    inst_period: float
    species_jp: str
    species: str
    family: str
    order: str
    wdry: Optional[float]
    number: Optional[float]
    prop_viable: Optional[float]
    pid: int


class SeedAnnualCreate(SeedAnnualBase):
    pass


class SeedAnnualInDB(SeedAnnualBase):
    id: int


class SeedAnnual(SeedAnnualBase):
    id: int
