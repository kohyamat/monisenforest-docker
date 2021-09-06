from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.database import get_crud
from app.crud import Crud
from app.schemas.seed_annual import SeedAnnual

router = APIRouter()


@router.get(
    "/",
    response_model=List[SeedAnnual],
    name="seed_annual: get_values_by_plotId",
)
async def get_seed_annual_by_plotid(
    plot_id: str,
    crud: Crud = Depends(get_crud(Crud)),
) -> List[SeedAnnual]:
    return await crud.get_seed_annual_by_plotid(plot_id=plot_id)
