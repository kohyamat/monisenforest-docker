from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.database import get_crud
from app.crud import Crud
from app.schemas.litter_annual import LitterAnnual

router = APIRouter()


@router.get(
    "/",
    response_model=List[LitterAnnual],
    name="litter_annual: get_values_by_plotId",
)
async def get_litter_annual_by_plotid(
    plot_id: str,
    crud: Crud = Depends(get_crud(Crud)),
) -> List[LitterAnnual]:
    return await crud.get_litter_annual_by_plotid(plot_id=plot_id)
