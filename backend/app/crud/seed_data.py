from typing import Any, Dict, List

from app.crud.base import CrudBase
from app.schemas.seed_annual import SeedAnnual
from app.schemas.seed_each import SeedEach

CREATE_SEED_ANNUAL_MANY_QUERY = """
    INSERT INTO seed_annual (
      year, t1, t2, inst_period, species_jp, species, family, "order",
      wdry, number, prop_viable, pid
    )
    VALUES (
      :year, :t1, :t2, :inst_period, :species_jp, :species, :family, :order,
      :wdry, :number, :prop_viable, :pid
    )
"""

GET_SEED_ANNUAL_BY_PID = """
    SELECT * FROM seed_annual
    WHERE pid=:pid;
"""

GET_SEED_ANNUAL_BY_PLOTID_QUERY = """
    SELECT * FROM seed_annual
    WHERE pid=(SELECT id FROM plots WHERE plot_id=:plot_id AND dtype='seed');
"""

DELETE_SEED_ANNUAL_BY_ID_QUERY = """
    DELETE FROM seed_annual
    WHERE pid=:pid
    RETURNING pid;
"""

CREATE_SEED_EACH_MANY_QUERY = """
    INSERT INTO seed_each (
      year, t1, t2, inst_period, species_jp, species, family, "order",
      wdry, number, prop_viable, pid
    )
    VALUES (
      :year, :t1, :t2, :inst_period, :species_jp, :species, :family, :order,
      :wdry, :number, :prop_viable, :pid
    )
"""

GET_SEED_EACH_BY_PID = """
    SELECT * FROM seed_each
    WHERE pid=:pid;
"""

GET_SEED_EACH_BY_PLOTID_QUERY = """
    SELECT * FROM seed_each
    WHERE pid=(SELECT id FROM plots WHERE plot_id=:plot_id AND dtype='seed');
"""

DELETE_SEED_EACH_BY_ID_QUERY = """
    DELETE FROM seed_each
    WHERE pid=:pid
    RETURNING pid;
"""


class CrudSeedData(CrudBase):
    async def create_seed_annual_many(
        self, *, query_values: List[Dict[Any, Any]]
    ) -> None:
        await self.db.execute_many(
            query=CREATE_SEED_ANNUAL_MANY_QUERY, values=query_values
        )

    async def get_seed_annual_by_pid(self, *, pid: int) -> List[SeedAnnual]:
        return_values = await self.db.fetch_all(
            query=GET_SEED_ANNUAL_BY_PID,
            values={"pid": pid},
        )
        return [SeedAnnual(**v) for v in return_values]

    async def get_seed_annual_by_plotid(self, *, plot_id: str) -> List[SeedAnnual]:
        return_values = await self.db.fetch_all(
            query=GET_SEED_ANNUAL_BY_PLOTID_QUERY,
            values={"plot_id": plot_id},
        )
        return [SeedAnnual(**v) for v in return_values]

    async def delete_seed_annual_by_pid(self, *, pid: int) -> int:
        return_values = await self.get_seed_annual_by_pid(pid=pid)
        if not return_values:
            return -1
        deleted_id = await self.db.execute(
            query=DELETE_SEED_ANNUAL_BY_ID_QUERY, values={"pid": pid}
        )
        return deleted_id

    async def create_seed_each_many(
        self, *, query_values: List[Dict[Any, Any]]
    ) -> None:
        await self.db.execute_many(
            query=CREATE_SEED_EACH_MANY_QUERY, values=query_values
        )

    async def get_seed_each_by_pid(self, *, pid: int) -> List[SeedEach]:
        return_values = await self.db.fetch_all(
            query=GET_SEED_EACH_BY_PID,
            values={"pid": pid},
        )
        return [SeedEach(**v) for v in return_values]

    async def get_seed_each_by_plotid(self, *, plot_id: str) -> List[SeedEach]:
        return_values = await self.db.fetch_all(
            query=GET_SEED_EACH_BY_PLOTID_QUERY,
            values={"plot_id": plot_id},
        )
        return [SeedEach(**v) for v in return_values]

    async def delete_seed_each_by_pid(self, *, pid: int) -> int:
        return_values = await self.get_seed_each_by_pid(pid=pid)
        if not return_values:
            return -1
        deleted_id = await self.db.execute(
            query=DELETE_SEED_EACH_BY_ID_QUERY, values={"pid": pid}
        )
        return deleted_id
