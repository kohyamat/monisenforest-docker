from typing import Any, Dict, List

from app.crud.base import CrudBase
from app.schemas.tree_com_summary import TreeComSummary
from app.schemas.tree_com_turnover import TreeComTurnover
from app.schemas.tree_sp_summary import TreeSpSummary
from app.schemas.tree_sp_turnover import TreeSpTurnover

CREATE_TREE_COM_SUMMARY_MANY_QUERY = """
    INSERT INTO tree_com_summary (
      year, mdate, nstem, nsp, ba, b, shannon, richness, pid
    )
    VALUES (:year, :mdate, :nstem, :nsp, :ba, :b, :shannon, :richness, :pid)
"""

GET_TREE_COM_SUMMARY_BY_PID = """
    SELECT * FROM tree_com_summary
    WHERE pid=:pid;
"""

GET_TREE_COM_SUMMARY_BY_PLOTID_QUERY = """
    SELECT * FROM tree_com_summary
    WHERE pid=(SELECT id FROM plots WHERE plot_id=:plot_id AND dtype='treeGBH');
"""

DELETE_TREE_COM_SUMMARY_BY_ID_QUERY = """
    DELETE FROM tree_com_summary
    WHERE pid=:pid
    RETURNING pid;
"""

CREATE_TREE_COM_TURNOVER_MANY_QUERY = """
    INSERT INTO tree_com_turnover (
      t1, t2, n_m, b_m, r_rel, m_rel, p_rel, l_rel,
      r_abs, m_abs, p_abs, l_abs, pid
    )
    VALUES (
      :t1, :t2, :n_m, :b_m, :r_rel, :m_rel, :p_rel, :l_rel,
      :r_abs, :m_abs, :p_abs, :l_abs, :pid
    )
"""

GET_TREE_COM_TURNOVER_BY_PID = """
    SELECT * FROM tree_com_turnover
    WHERE pid=:pid;
"""

GET_TREE_COM_TURNOVER_BY_PLOTID_QUERY = """
    SELECT * FROM tree_com_turnover
    WHERE pid=(SELECT id FROM plots WHERE plot_id=:plot_id AND dtype='treeGBH');
"""

DELETE_TREE_COM_TURNOVER_BY_ID_QUERY = """
    DELETE FROM tree_com_turnover
    WHERE pid=:pid
    RETURNING pid;
"""

CREATE_TREE_SP_SUMMARY_MANY_QUERY = """
    INSERT INTO tree_sp_summary (
      year, species_jp, species, family, "order",
      n, ba, b, n_prop, ba_prop, b_prop, pid
    )
    VALUES (
      :year, :species_jp, :species, :family, :order,
      :n, :ba, :b, :n_prop, :ba_prop, :b_prop, :pid
    )
"""

GET_TREE_SP_SUMMARY_BY_PID = """
    SELECT * FROM tree_sp_summary
    WHERE pid=:pid;
"""

GET_TREE_SP_SUMMARY_BY_PLOTID_QUERY = """
    SELECT * FROM tree_sp_summary
    WHERE pid=(SELECT id FROM plots WHERE plot_id=:plot_id AND dtype='treeGBH');
"""

DELETE_TREE_SP_SUMMARY_BY_ID_QUERY = """
    DELETE FROM tree_sp_summary
    WHERE pid=:pid
    RETURNING pid;
"""

CREATE_TREE_SP_TURNOVER_MANY_QUERY = """
    INSERT INTO tree_sp_turnover (
      t1, t2, species_jp, species, family, "order", n_m, b_m,
      r_rel, m_rel, p_rel, l_rel, r_abs, m_abs, p_abs, l_abs, pid
    )
    VALUES (
      :t1, :t2, :species_jp, :species, :family, :order, :n_m, :b_m,
      :r_rel, :m_rel, :p_rel, :l_rel, :r_abs, :m_abs, :p_abs, :l_abs, :pid
    )
"""

GET_TREE_SP_TURNOVER_BY_PID = """
    SELECT * FROM tree_sp_turnover
    WHERE pid=:pid;
"""

GET_TREE_SP_TURNOVER_BY_PLOTID_QUERY = """
    SELECT * FROM tree_sp_turnover
    WHERE pid=(SELECT id FROM plots WHERE plot_id=:plot_id AND dtype='treeGBH');
"""

DELETE_TREE_SP_TURNOVER_BY_ID_QUERY = """
    DELETE FROM tree_sp_turnover
    WHERE pid=:pid
    RETURNING pid;
"""

GET_TREE_SP_LIST_QUERY = """
    SELECT species, species_jp FROM tree_sp_summary;
"""

GET_TREE_SP_OCCURRENCE_QUERY = """
    SELECT pid, species FROM tree_sp_summary
    WHERE species=:species;
"""


class CrudTreeData(CrudBase):
    async def create_tree_com_summary_many(
        self, *, query_values: List[Dict[Any, Any]]
    ) -> None:
        await self.db.execute_many(
            query=CREATE_TREE_COM_SUMMARY_MANY_QUERY, values=query_values
        )

    async def get_tree_com_summary_by_pid(self, *, pid: int) -> List[TreeComSummary]:
        return_values = await self.db.fetch_all(
            query=GET_TREE_COM_SUMMARY_BY_PID,
            values={"pid": pid},
        )
        return [TreeComSummary(**v) for v in return_values]

    async def get_tree_com_summary_by_plotid(
        self, *, plot_id: str
    ) -> List[TreeComSummary]:
        return_values = await self.db.fetch_all(
            query=GET_TREE_COM_SUMMARY_BY_PLOTID_QUERY,
            values={"plot_id": plot_id},
        )
        return [TreeComSummary(**v) for v in return_values]

    async def delete_tree_com_summary_by_pid(self, *, pid: int) -> int:
        return_values = await self.get_tree_com_summary_by_pid(pid=pid)
        if not return_values:
            return -1
        deleted_id = await self.db.execute(
            query=DELETE_TREE_COM_SUMMARY_BY_ID_QUERY, values={"pid": pid}
        )
        return deleted_id

    async def create_tree_com_turnover_many(
        self, *, query_values: List[Dict[Any, Any]]
    ) -> None:
        await self.db.execute_many(
            query=CREATE_TREE_COM_TURNOVER_MANY_QUERY, values=query_values
        )

    async def get_tree_com_turnover_by_pid(self, *, pid: int) -> List[TreeComTurnover]:
        return_values = await self.db.fetch_all(
            query=GET_TREE_COM_TURNOVER_BY_PID,
            values={"pid": pid},
        )
        return [TreeComTurnover(**v) for v in return_values]

    async def get_tree_com_turnover_by_plotid(
        self, *, plot_id: str
    ) -> List[TreeComTurnover]:
        return_values = await self.db.fetch_all(
            query=GET_TREE_COM_TURNOVER_BY_PLOTID_QUERY,
            values={"plot_id": plot_id},
        )
        return [TreeComTurnover(**v) for v in return_values]

    async def delete_tree_com_turnover_by_pid(self, *, pid: int) -> int:
        return_values = await self.get_tree_com_turnover_by_pid(pid=pid)
        if not return_values:
            return -1
        deleted_id = await self.db.execute(
            query=DELETE_TREE_COM_TURNOVER_BY_ID_QUERY, values={"pid": pid}
        )
        return deleted_id

    async def create_tree_sp_summary_many(
        self, *, query_values: List[Dict[Any, Any]]
    ) -> None:
        await self.db.execute_many(
            query=CREATE_TREE_SP_SUMMARY_MANY_QUERY, values=query_values
        )

    async def get_tree_sp_summary_by_pid(self, *, pid: int) -> List[TreeSpSummary]:
        return_values = await self.db.fetch_all(
            query=GET_TREE_SP_SUMMARY_BY_PID,
            values={"pid": pid},
        )
        return [TreeSpSummary(**v) for v in return_values]

    async def get_tree_sp_summary_by_plotid(
        self, *, plot_id: str
    ) -> List[TreeSpSummary]:
        return_values = await self.db.fetch_all(
            query=GET_TREE_SP_SUMMARY_BY_PLOTID_QUERY,
            values={"plot_id": plot_id},
        )
        return [TreeSpSummary(**v) for v in return_values]

    async def delete_tree_sp_summary_by_pid(self, *, pid: int) -> int:
        return_values = await self.get_tree_sp_summary_by_pid(pid=pid)
        if not return_values:
            return -1
        deleted_id = await self.db.execute(
            query=DELETE_TREE_SP_SUMMARY_BY_ID_QUERY, values={"pid": pid}
        )
        return deleted_id

    async def create_tree_sp_turnover_many(
        self, *, query_values: List[Dict[Any, Any]]
    ) -> None:
        await self.db.execute_many(
            query=CREATE_TREE_SP_TURNOVER_MANY_QUERY, values=query_values
        )

    async def get_tree_sp_turnover_by_pid(self, *, pid: int) -> List[TreeSpTurnover]:
        return_values = await self.db.fetch_all(
            query=GET_TREE_SP_TURNOVER_BY_PID,
            values={"pid": pid},
        )
        return [TreeSpTurnover(**v) for v in return_values]

    async def get_tree_sp_turnover_by_plotid(
        self, *, plot_id: str
    ) -> List[TreeSpTurnover]:
        return_values = await self.db.fetch_all(
            query=GET_TREE_SP_TURNOVER_BY_PLOTID_QUERY,
            values={"plot_id": plot_id},
        )
        return [TreeSpTurnover(**v) for v in return_values]

    async def delete_tree_sp_turnover_by_pid(self, *, pid: int) -> int:
        return_values = await self.get_tree_sp_turnover_by_pid(pid=pid)
        if not return_values:
            return -1
        deleted_id = await self.db.execute(
            query=DELETE_TREE_SP_TURNOVER_BY_ID_QUERY, values={"pid": pid}
        )
        return deleted_id

    async def get_tree_sp_list(self) -> List[Dict[Any, Any]]:
        return_values = await self.db.fetch_all(query=GET_TREE_SP_LIST_QUERY)
        res = []
        for x in return_values:
            sp = {"species": x["species"], "name_jp": x["species_jp"]}
            if sp not in res:
                res.append(sp)
        return res

    async def get_tree_sp_occurrence(self, *, species: str) -> List[int]:
        return_values = await self.db.fetch_all(
            query=GET_TREE_SP_OCCURRENCE_QUERY, values={"species": species}
        )
        res = []
        for x in return_values:
            if x["pid"] not in res:
                res.append(x["pid"])
        return res
