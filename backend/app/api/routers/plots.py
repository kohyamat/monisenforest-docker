from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

import app.base as base
from app.api.dependencies.database import get_crud
from app.api.routers.upload_file import create_data_summary
from app.crud import Crud
from app.schemas.plot import Plot, PlotCreate, PlotUpdate

# from starlette.status import HTTP_201_CREATED

router = APIRouter()


@router.get(
    "/",
    response_model=List[Plot],
    name="plots: get_all",
)
async def get_all_plots(
    crud: Crud = Depends(get_crud(Crud)),
) -> List[Plot]:
    return await crud.get_all_plots()


@router.get(
    "/{id}/",
    response_model=Plot,
    name="plots: get_one_by_id",
)
async def get_plot_by_id(
    id: int,
    crud: Crud = Depends(get_crud(Crud)),
) -> Optional[Plot]:
    plot = await crud.get_plot_by_id(id=id)
    return plot


# @router.post(
#     "/",
#     response_model=Plot,
#     name="plots: create_new",
#     status_code=HTTP_201_CREATED,
# )
# async def create_plot(
#     new_plot: PlotCreate = Body(..., embed=True),
#     crud: Crud = Depends(get_crud(Crud)),
# ) -> Plot:
#     plot = await crud.create_plot(new_plot=new_plot)
#     return plot


@router.delete(
    "/{id}/",
    response_model=int,
    name="plots: delete_one_by_id",
)
async def delete_plot_by_id(
    id: int,
    crud: Crud = Depends(get_crud(Crud)),
) -> int:
    deleted_plot = await crud.delete_plot_by_id(id=id)
    return deleted_plot


@router.put(
    "/{id}/",
    name="plots: update",
)
async def update_plot(
    id: int,
    plot_update: PlotUpdate,
    crud: Crud = Depends(get_crud(Crud)),
) -> Optional[Plot]:

    plot_update_dict = plot_update.dict()
    tmppath = plot_update_dict.pop("tmppath")
    tmppath = Path(tmppath)
    plot = await crud.update_plot(id=id, plot_update=PlotCreate(**plot_update_dict))
    if plot is not None:
        await delete_data_summary(id=id, dtype=plot.dtype, crud=crud)
        try:
            with tmppath.open("rb") as tmp:
                d = base.read_data(tmp.read())
            await create_data_summary(pid=id, dtype=plot.dtype, d=d, crud=crud)
        except Exception as e:
            raise HTTPException(
                status_code=406,
                detail="Could not parse {}: {}".format(plot.filename, e),
            )
        finally:
            tmppath.unlink()

    return plot


async def delete_data_summary(id: int, dtype: str, crud: Crud):
    if dtype == "treeGBH":
        await crud.delete_tree_com_summary_by_pid(pid=id)
        await crud.delete_tree_com_turnover_by_pid(pid=id)
        await crud.delete_tree_sp_summary_by_pid(pid=id)
        await crud.delete_tree_sp_turnover_by_pid(pid=id)
    elif dtype == "litter":
        await crud.delete_litter_each_by_pid(pid=id)
        await crud.delete_litter_annual_by_pid(pid=id)
    elif dtype == "seed":
        await crud.delete_seed_each_by_pid(pid=id)
        await crud.delete_seed_annual_by_pid(pid=id)
    else:
        pass
