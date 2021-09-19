from typing import List, Optional

from app import models, schemas
from app.db.db import get_session
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.TreeComTurnover],
    name="tree_com_turnover: get_values_by_plotId",
)
async def get_tree_com_turnover(
    plot_id: str, session: AsyncSession = Depends(get_session)
) -> Optional[List[schemas.TreeComTurnover]]:
    result = await session.execute(
        select(models.Datafile)
        .where(models.Datafile.plot_id == plot_id)
        .where(models.Datafile.dtype == "treeGBH")
        .options(selectinload(models.Datafile.tree_com_turnover))
    )
    datafile = result.scalars().first()
    if datafile:
        return sorted(datafile.tree_com_turnover, key=lambda x: x.id)
    else:
        return None


@router.get(
    "/all/",
    response_model=List[schemas.TreeComTurnover],
    name="tree_com_turnover: get_all",
)
async def get_tree_com_turnover_all(
    session: AsyncSession = Depends(get_session),
) -> Optional[List[schemas.TreeComTurnover]]:
    result = await session.execute(
        select(models.TreeComTurnover).order_by(models.TreeComTurnover.id)
    )
    return result.scalars().all()
