from typing import Any, Dict, List

from app.crud.base import CrudBase
from app.schemas.litter_annual import LitterAnnual
from app.schemas.litter_each import LitterEach 

CREATE_LITTER_ANNUAL_MANY_QUERY = """
    INSERT INTO litter_annual (
      year, n_collect, t1, t2, inst_period,
      wdry_leaf, wdry_branch, wdry_rep, wdry_all, pid
    )
    VALUES (
      :year, :n_collect, :t1, :t2, :inst_period,
      :wdry_leaf, :wdry_branch, :wdry_rep, :wdry_all, :pid
    )
"""

GET_LITTER_ANNUAL_BY_PID = """
    SELECT * FROM litter_annual
    WHERE pid=:pid;
"""

GET_LITTER_ANNUAL_BY_PLOTID_QUERY = """
    SELECT * FROM litter_annual
    WHERE pid=(SELECT id FROM plots WHERE plot_id=:plot_id AND dtype='litter');
"""

DELETE_LITTER_ANNUAL_BY_ID_QUERY = """
    DELETE FROM litter_annual
    WHERE pid=:pid
    RETURNING pid;
"""

CREATE_LITTER_EACH_MANY_QUERY = """
    INSERT INTO litter_each (
      year, t1, t2, inst_period,
      wdry_leaf, wdry_branch, wdry_rep, wdry_all, pid
    )
    VALUES (
      :year, :t1, :t2, :inst_period,
      :wdry_leaf, :wdry_branch, :wdry_rep, :wdry_all, :pid
    )
"""

GET_LITTER_EACH_BY_PID = """
    SELECT * FROM litter_each
    WHERE pid=:pid;
"""

GET_LITTER_EACH_BY_PLOTID_QUERY = """
    SELECT * FROM litter_each
    WHERE pid=(SELECT id FROM plots WHERE plot_id=:plot_id AND dtype='litter');
"""

DELETE_LITTER_EACH_BY_ID_QUERY = """
    DELETE FROM litter_each
    WHERE pid=:pid
    RETURNING pid;
"""


class CrudLitterData(CrudBase):
    async def create_litter_annual_many(
        self, *, query_values: List[Dict[Any, Any]]
    ) -> None:
        await self.db.execute_many(
            query=CREATE_LITTER_ANNUAL_MANY_QUERY, values=query_values
        )

    async def get_litter_annual_by_pid(self, *, pid: int) -> List[LitterAnnual]:
        return_values = await self.db.fetch_all(
            query=GET_LITTER_ANNUAL_BY_PID,
            values={"pid": pid},
        )
        return [LitterAnnual(**v) for v in return_values]

    async def get_litter_annual_by_plotid(
        self, *, plot_id: str
    ) -> List[LitterAnnual]:
        return_values = await self.db.fetch_all(
            query=GET_LITTER_ANNUAL_BY_PLOTID_QUERY,
            values={"plot_id": plot_id},
        )
        return [LitterAnnual(**v) for v in return_values]

    async def delete_litter_annual_by_pid(self, *, pid: int) -> int:
        return_values = await self.get_litter_annual_by_pid(pid=pid)
        if not return_values:
            return -1
        deleted_id = await self.db.execute(
            query=DELETE_LITTER_ANNUAL_BY_ID_QUERY, values={"pid": pid}
        )
        return deleted_id

    async def create_litter_each_many(
        self, *, query_values: List[Dict[Any, Any]]
    ) -> None:
        await self.db.execute_many(
            query=CREATE_LITTER_EACH_MANY_QUERY, values=query_values
        )

    async def get_litter_each_by_pid(self, *, pid: int) -> List[LitterEach]:
        return_values = await self.db.fetch_all(
            query=GET_LITTER_EACH_BY_PID,
            values={"pid": pid},
        )
        return [LitterEach(**v) for v in return_values]

    async def get_litter_each_by_plotid(
        self, *, plot_id: str
    ) -> List[LitterEach]:
        return_values = await self.db.fetch_all(
            query=GET_LITTER_EACH_BY_PLOTID_QUERY,
            values={"plot_id": plot_id},
        )
        return [LitterEach(**v) for v in return_values]

    async def delete_litter_each_by_pid(self, *, pid: int) -> int:
        return_values = await self.get_litter_each_by_pid(pid=pid)
        if not return_values:
            return -1
        deleted_id = await self.db.execute(
            query=DELETE_LITTER_EACH_BY_ID_QUERY, values={"pid": pid}
        )
        return deleted_id
