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
    response_model=List[schemas.TreeSpSummary],
    name="tree_sp_summary: get_values_by_plotId",
)
async def get_tree_sp_summary(
    plot_id: str, session: AsyncSession = Depends(get_session)
) -> Optional[List[schemas.TreeSpSummary]]:
    result = await session.execute(
        select(models.Datafile)
        .where(models.Datafile.plot_id == plot_id)
        .where(models.Datafile.dtype == 'treeGBH')
        .options(selectinload(models.Datafile.tree_sp_summary))
    )
    datafile = result.scalars().first()
    if datafile:
        return datafile.tree_sp_summary
    else:
        return None

