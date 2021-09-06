from typing import List, Optional

from app.api.dependencies.database import get_crud
from app.crud import Crud
from app.schemas.tree_sp_summary import TreeSpSummary
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/",
    response_model=List[TreeSpSummary],
    name="tree_sp_summary: get_values_by_plotId",
)
async def get_tree_sp_summary_by_plotid(
    plot_id: str,
    crud: Crud = Depends(get_crud(Crud)),
) -> List[TreeSpSummary]:
    return await crud.get_tree_sp_summary_by_plotid(plot_id=plot_id)


@router.get(
    "/{pid}/",
    response_model=TreeSpSummary,
    name="tree_sp_summary: get_one_by_id",
)
async def get_plot_by_id(
    pid: int,
    crud: Crud = Depends(get_crud(Crud)),
) -> Optional[TreeSpSummary]:
    return await crud.get_tree_sp_summary_by_pid(pid=pid)
