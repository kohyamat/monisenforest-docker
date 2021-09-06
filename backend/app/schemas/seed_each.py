from typing import Optional

from pydantic import BaseModel


class SeedEachBase(BaseModel):
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


class SeedEachCreate(SeedEachBase):
    pass


class SeedEachInDB(SeedEachBase):
    id: int


class SeedEach(SeedEachBase):
    id: int
