from typing import Any, Dict, List

from app.api.dependencies.database import get_crud
from app.crud import Crud
from app.schemas.tree_sp_summary import TreeSpSummary
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/list/", response_model=List[Dict[Any, Any]], name="species: get_species_list"
)
async def get_tree_sp_list(
    crud: Crud = Depends(get_crud(Crud)),
) -> List[Dict[Any, Any]]:
    return await crud.get_tree_sp_list()


@router.get(
    "/occurrence/", response_model=List[str], name="species: get_species_occurence"
)
async def get_tree_sp_occurrence(
    species: str,
    crud: Crud = Depends(get_crud(Crud)),
) -> List[str]:
    plots = await crud.get_all_plots()
    print(plots)
    plot_id_dict = {p.id: p.plot_id for p in plots}
    return_values = await crud.get_tree_sp_occurrence(species=species)
    return [plot_id_dict[i] for i in return_values]
