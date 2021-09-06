from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.database import get_crud
from app.crud import Crud
from app.schemas.seed_each import SeedEach

router = APIRouter()


@router.get(
    "/",
    response_model=List[SeedEach],
    name="seed_each: get_values_by_plotId",
)
async def get_seed_each_by_plotid(
    plot_id: str,
    crud: Crud = Depends(get_crud(Crud)),
) -> List[SeedEach]:
    return await crud.get_seed_each_by_plotid(plot_id=plot_id)
