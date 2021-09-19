from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app import models, schemas
from app.db.db import get_session

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.LitterEach],
    name="litter_each: get_values_by_plotId",
)
async def get_litter_each(
    plot_id: str, session: AsyncSession = Depends(get_session)
) -> Optional[List[schemas.LitterEach]]:
    result = await session.execute(
        select(models.Datafile)
        .where(models.Datafile.plot_id == plot_id)
        .where(models.Datafile.dtype == 'litter')
        .options(selectinload(models.Datafile.litter_each))
    )
    datafile = result.scalars().first()
    if datafile:
        return sorted(datafile.litter_each, key=lambda x: x.id)
    else:
        return None


@router.get(
    "/all/",
    response_model=List[schemas.LitterEach],
    name="litter_each: get_all",
)
async def get_litter_each_all(
    session: AsyncSession = Depends(get_session),
) -> Optional[List[schemas.LitterEach]]:
    result = await session.execute(
        select(models.LitterEach).order_by(models.LitterEach.id)
    )
    return result.scalars().all()
