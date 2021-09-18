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
    response_model=List[schemas.SeedEach],
    name="seed_each: get_values_by_plotId",
)
async def get_seed_each(
    plot_id: str, session: AsyncSession = Depends(get_session)
) -> Optional[List[schemas.SeedEach]]:
    result = await session.execute(
        select(models.Datafile)
        .where(models.Datafile.plot_id == plot_id)
        .where(models.Datafile.dtype == 'seed')
        .options(selectinload(models.Datafile.seed_each))
    )
    datafile = result.scalars().first()
    if datafile:
        return sorted(datafile.seed_each, key=lambda x: x.id)
    else:
        return None
