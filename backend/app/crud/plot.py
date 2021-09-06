from typing import List, Union

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.crud.base import CrudBase
from app.schemas.plot import Plot, PlotCreate

CREATE_PLOT_QUERY = """
    INSERT INTO plots (plot_id, name, name_jp, filename, md5, dtype, date, size)
    VALUES (:plot_id, :name, :name_jp, :filename, :md5, :dtype, :date, :size)
    RETURNING id, plot_id, name, name_jp, filename, md5, dtype, date, size;
"""

GET_PLOT_BY_ID_QUERY = """
    SELECT id, plot_id, name, name_jp, filename, md5, dtype, date, size
    FROM plots
    WHERE id=:id;
"""

GET_PLOT_BY_PLOTID_AND_DTYPE_QUERY = """
    SELECT id, plot_id, name, name_jp, filename, md5, dtype, date, size
    FROM plots
    WHERE plot_id=:plot_id AND dtype=:dtype;
"""

GET_ALL_PLOTS_QUERY = """
    SELECT id, plot_id, name, name_jp, filename, md5, dtype, date, size
    FROM plots;
"""

UPDATE_PLOT_BY_ID_QUERY = """
    UPDATE plots
    SET plot_id=:plot_id,
        name=:name,
        name_jp=:name_jp,
        filename=:filename,
        md5=:md5,
        dtype=:dtype,
        date=:date,
        size=:size
    WHERE id = :id
    RETURNING id, plot_id, name, name_jp, filename, md5, dtype, date, size;
"""

DELETE_PLOT_BY_ID_QUERY = """
    DELETE FROM plots
    WHERE id=:id
    RETURNING id;
"""


class CrudPlot(CrudBase):
    async def create_plot(self, *, new_plot: PlotCreate) -> Plot:
        query_values = new_plot.dict()
        plot = await self.db.fetch_one(query=CREATE_PLOT_QUERY, values=query_values)
        return Plot(**plot)

    async def get_plot_by_id(self, *, id: int) -> Union[Plot, None]:
        plot = await self.db.fetch_one(query=GET_PLOT_BY_ID_QUERY, values={"id": id})
        if not plot:
            return None
        return Plot(**plot)

    async def get_plot_by_plotid_and_dtype(
        self, *, plot_id: str, dtype: str
    ) -> Union[Plot, None]:
        plot = await self.db.fetch_one(
            query=GET_PLOT_BY_PLOTID_AND_DTYPE_QUERY,
            values={"plot_id": plot_id, "dtype": dtype},
        )
        if not plot:
            return None
        return Plot(**plot)

    async def get_all_plots(self) -> List[Plot]:
        plots = await self.db.fetch_all(query=GET_ALL_PLOTS_QUERY)
        return [Plot(**item) for item in plots]

    async def update_plot(
        self, *, id: int, plot_update: PlotCreate
    ) -> Union[Plot, None]:
        plot = await self.get_plot_by_id(id=id)
        if not plot:
            return None
        plot_update_params = plot.copy(update=plot_update.dict(exclude_unset=True))
        try:
            updated_plot = await self.db.fetch_one(
                query=UPDATE_PLOT_BY_ID_QUERY, values=plot_update_params.dict()
            )
            return Plot(**updated_plot)
        except Exception:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Invalid update params."
            )

    async def delete_plot_by_id(self, *, id: int) -> int:
        plot = await self.get_plot_by_id(id=id)
        if not plot:
            return -1
        deleted_id = await self.db.execute(
            query=DELETE_PLOT_BY_ID_QUERY, values={"id": id}
        )
        return deleted_id
