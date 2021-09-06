from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.database import get_crud
from app.crud import Crud
from app.schemas.tree_com_turnover import TreeComTurnover

router = APIRouter()


@router.get(
    "/",
    response_model=List[TreeComTurnover],
    name="tree_com_turnover: get_values_by_plotId",
)
async def get_tree_com_turnover_by_plotid(
    plot_id: str,
    crud: Crud = Depends(get_crud(Crud)),
) -> List[TreeComTurnover]:
    return await crud.get_tree_com_turnover_by_plotid(plot_id=plot_id)
