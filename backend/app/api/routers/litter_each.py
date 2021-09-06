from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.database import get_crud
from app.crud import Crud
from app.schemas.litter_each import LitterEach

router = APIRouter()


@router.get(
    "/",
    response_model=List[LitterEach],
    name="litter_each: get_values_by_plotId",
)
async def get_litter_each_by_plotid(
    plot_id: str,
    crud: Crud = Depends(get_crud(Crud)),
) -> List[LitterEach]:
    return await crud.get_litter_each_by_plotid(plot_id=plot_id)
