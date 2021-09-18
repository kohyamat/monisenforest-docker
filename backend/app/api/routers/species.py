from typing import Any, Dict, List

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models, schemas
from app.db.db import get_session

router = APIRouter()


@router.get(
    "/list/", response_model=List[Dict[Any, Any]], name="species: get_species_list"
)
async def get_tree_sp_list(
    session: AsyncSession = Depends(get_session),
) -> List[Dict[Any, Any]]:
    result = await session.execute(
        select(models.TreeSpSummary.species, models.TreeSpSummary.species_jp)
    )
    species_list = []
    for x in result:
        sp = {"species": x[0], "name_jp": x[1]}
        if sp not in species_list:
            species_list.append(sp)
    return species_list


@router.get(
    "/occurrence/",
    response_model=List[str],
    name="species: get_species_occurence",
)
async def get_tree_sp_occurrence(
    species: str,
    session: AsyncSession = Depends(get_session),
) -> List[str]:
    result = await session.execute(select(models.Datafile))
    datafiles = result.scalars().all()
    plot_id_dict = {x.id: x.plot_id for x in datafiles}
    query = select(models.TreeSpSummary.datafile_id).where(
        models.TreeSpSummary.species == species
    )
    result = await session.execute(query)
    return [plot_id_dict[i] for i in set([i[0] for i in result])]
