from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.database import get_crud
from app.crud import Crud
from app.schemas.tree_sp_turnover import TreeSpTurnover

router = APIRouter()


@router.get(
    "/",
    response_model=List[TreeSpTurnover],
    name="tree_sp_turnover: get_values_by_plotId",
)
async def get_tree_sp_turnover_by_plotid(
    plot_id: str,
    crud: Crud = Depends(get_crud(Crud)),
) -> List[TreeSpTurnover]:
    return await crud.get_tree_sp_turnover_by_plotid(plot_id=plot_id)
