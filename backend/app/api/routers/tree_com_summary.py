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
    response_model=List[schemas.TreeComSummary],
    name="tree_com_summary: get_values_by_plotId",
)
async def get_tree_com_summary(
    plot_id: str, session: AsyncSession = Depends(get_session)
) -> Optional[List[schemas.TreeComSummary]]:
    result = await session.execute(
        select(models.Datafile)
        .where(models.Datafile.plot_id == plot_id)
        .where(models.Datafile.dtype == 'treeGBH')
        .options(selectinload(models.Datafile.tree_com_summary))
    )
    datafile = result.scalars().first()
    if datafile:
        return sorted(datafile.tree_com_summary, key=lambda x: x.id)
    else:
        return None
