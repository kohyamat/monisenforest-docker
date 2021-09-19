import hashlib
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List, Optional

import app.base as base
import app.summarise as summarise
from app import models, schemas
from app.db.db import get_session
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_201_CREATED

router = APIRouter()


class DataExistsException(Exception):
    def __init__(self, id: int, data: Dict[Any, Any]):
        self.id = id
        self.data = data


@router.get(
    "/",
    response_model=List[schemas.Datafile],
    name="datafiles: get_all",
)
async def get_datafiles(
    session: AsyncSession = Depends(get_session),
) -> List[schemas.Datafile]:
    result = await session.execute(select(models.Datafile))
    datafiles = result.scalars().all()
    return datafiles


@router.get(
    "/filter/",
    response_model=List[schemas.Datafile],
    name="datafiles: get_all",
)
async def get_datafile_by_plotid_and_dtype(
    plot_id: Optional[str] = None,
    dtype: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
) -> Optional[schemas.Datafile]:
    result = await session.execute(
        select(models.Datafile)
        .where(models.Datafile.plot_id == plot_id)
        .where(models.Datafile.dtype == dtype)
    )
    return result.scalars().first()


@router.get(
    "/{id}",
    response_model=schemas.Datafile,
    name="datafiles: get_one_by_id",
)
async def get_datafile_by_id(
    id: int,
    session: AsyncSession = Depends(get_session),
) -> Optional[schemas.Datafile]:
    result = await session.execute(
        select(models.Datafile).where(models.Datafile.id == id)
    )
    return result.scalars().first()


@router.post(
    "/",
    response_model=schemas.Datafile,
    name="datafiles: create_new",
    status_code=HTTP_201_CREATED,
)
async def add_datafile(
    datafileIn: schemas.DatafileCreate = Body(..., embed=True),
    session: AsyncSession = Depends(get_session),
) -> schemas.Datafile:
    datafile = models.Datafile(**dict(datafileIn))
    session.add(datafile)
    await session.commit()
    await session.refresh(datafile)
    return datafile


@router.delete(
    "/{id}/",
    name="datafiles: delete_one_by_id",
)
async def delete_datafile(
    id: int, session: AsyncSession = Depends(get_session)
) -> Dict[Any, Any]:
    query = delete(models.Datafile).where(models.Datafile.id == id)
    await session.execute(query)
    await session.commit()
    return {"Message": "Deleted id={} from 'datafiles'".format(id)}


@router.post(
    "/upload/",
    response_model=schemas.Datafile,
    name="upload_file: create_from_file",
    status_code=HTTP_201_CREATED,
)
async def upload_file(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
) -> schemas.Datafile:
    tmppath = await save_upload_file_tmp(file)

    with tmppath.open("rb") as tmp:
        contents = tmp.read()
        md5 = hashlib.md5(contents).hexdigest()

    d = base.read_data(contents, max_col=500)
    date, name, name_jp = parse_metadata(d)

    datafileIn = schemas.DatafileCreate(
        plot_id=d.plot_id,
        name=name,
        name_jp=name_jp,
        filename=file.filename,
        md5=md5,
        dtype=d.data_type,
        date=date,
        size=round(sys.getsizeof(contents) / 1024, 1),
    )

    datafile_in_db = await get_datafile_by_plotid_and_dtype(
        datafileIn.plot_id, datafileIn.dtype, session
    )

    if datafile_in_db:
        raise DataExistsException(
            id=datafile_in_db.id, data={**datafileIn.dict(), "tmppath": str(tmppath)}
        )
    else:
        tmppath.unlink()
        datafile = await add_datafile(datafileIn, session)
        try:
            await add_data_summary(datafile.id, datafile.dtype, d, session)
        except Exception as e:
            raise HTTPException(
                status_code=406,
                detail="Could not parse {}: {}".format(datafile.filename, e),
            )
        finally:
            return datafile


async def save_upload_file_tmp(file: UploadFile) -> Path:
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmppath = Path(tmp.name)
    finally:
        file.file.close()
    return tmppath


def parse_metadata(d: base.MonitoringData):
    date = ""
    if "DATA CREATED" in d.metadata:
        date_ = d.metadata["DATA CREATED"]
        try:
            if len(date_) == 8:
                date = datetime.strptime(date_, "%Y%m%d").strftime("%Y-%m-%d")
            elif len(date_) == 6:
                date = datetime.strptime(date_, "%y%m%d").strftime("%Y-%m-%d")
            else:
                date = "unknown"
        except ValueError:
            date = "unknown"

    name = ""
    r = re.compile(r".*at\s([A-Za-z\s\-\.]*)\s?\([A-Z]{2}-[A-Z]{2}[0-9]\)")
    if "DATA TITLE" in d.metadata:
        m = r.search(d.metadata["DATA TITLE"])
        if m:
            name = m.group(1).strip()

    pat = r"(^.*)[\(（].*[\)）]"
    if d.metadata["PLOT NAME"] != "-":
        name_jp = re.sub(pat, "\\1", d.metadata["PLOT NAME"]).strip()
    else:
        name_jp = re.sub(pat, "\\1", d.metadata["SITE NAME"]).strip()

    return date, name, name_jp


async def add_data_summary(
    datafile_id: int, dtype: str, d: base.MonitoringData, session: AsyncSession
) -> None:
    if dtype == "treeGBH":
        await add_tree_data_summary(datafile_id, d, session)
    elif dtype == "litter":
        await add_litter_data_summary(datafile_id, d, session)
    elif dtype == "seed":
        await add_seed_data_summary(datafile_id, d, session)
    else:
        pass


async def add_tree_data_summary(
    datafile_id: int,
    d: base.MonitoringData,
    session: AsyncSession,
) -> None:
    ts = summarise.TreeSummary(d)
    query_values = [
        dict({"datafile_id": datafile_id}, **x) for x in ts.species_summary()
    ]
    await session.execute(models.TreeSpSummary.__table__.insert(), query_values)
    await session.commit()

    query_values = [
        dict({"datafile_id": datafile_id}, **x) for x in ts.species_turnover()
    ]
    await session.execute(models.TreeSpTurnover.__table__.insert(), query_values)
    await session.commit()

    query_values = [
        dict({"datafile_id": datafile_id}, **x) for x in ts.community_summary()
    ]
    await session.execute(models.TreeComSummary.__table__.insert(), query_values)
    await session.commit()

    query_values = [
        dict({"datafile_id": datafile_id}, **x) for x in ts.community_turnover()
    ]
    await session.execute(models.TreeComTurnover.__table__.insert(), query_values)
    await session.commit()


async def add_litter_data_summary(
    datafile_id: int,
    d: base.MonitoringData,
    session: AsyncSession,
) -> None:
    ls = summarise.LitterSummary(d)
    query_values = [dict({"datafile_id": datafile_id}, **x) for x in ls.each_sampling()]
    await session.execute(models.LitterEach.__table__.insert(), query_values)
    await session.commit()

    query_values = [dict({"datafile_id": datafile_id}, **x) for x in ls.annual()]
    await session.execute(models.LitterAnnual.__table__.insert(), query_values)
    await session.commit()


async def add_seed_data_summary(
    datafile_id: int,
    d: base.MonitoringData,
    session: AsyncSession,
) -> None:
    ss = summarise.SeedSummary(d)
    query_values = [dict({"datafile_id": datafile_id}, **x) for x in ss.each_sampling()]
    await session.execute(models.SeedEach.__table__.insert(), query_values)
    await session.commit()

    query_values = [dict({"datafile_id": datafile_id}, **x) for x in ss.annual()]
    await session.execute(models.SeedAnnual.__table__.insert(), query_values)
    await session.commit()


@router.put(
    "/{id}/",
    name="datafiles: update",
)
async def update_plot(
    id: int,
    datafile_update: schemas.DatafileUpdate,
    session: AsyncSession = Depends(get_session),
) -> None:
    values = datafile_update.dict()
    tmppath = Path(values.pop("tmppath"))
    query = update(models.Datafile).where(models.Datafile.id == id).values(**values)
    await session.execute(query)
    await session.commit()
    await delete_data_summary(id, datafile_update.dtype, session)
    try:
        with tmppath.open("rb") as tmp:
            d = base.read_data(tmp.read(), max_col=500)
        await add_data_summary(id, datafile_update.dtype, d, session)
    except Exception as e:
        raise HTTPException(
            status_code=406,
            detail="Could not parse {}: {}".format(datafile_update.filename, e),
        )
    finally:
        tmppath.unlink()


async def delete_data_summary(id: int, dtype: str, session: AsyncSession) -> None:
    if dtype == "treeGBH":
        query = delete(models.TreeComSummary).where(
            models.TreeComSummary.datafile_id == id
        )
        await session.execute(query)
        query = delete(models.TreeComTurnover).where(
            models.TreeComTurnover.datafile_id == id
        )
        await session.execute(query)
        query = delete(models.TreeSpSummary).where(
            models.TreeSpSummary.datafile_id == id
        )
        await session.execute(query)
        query = delete(models.TreeSpTurnover).where(
            models.TreeSpTurnover.datafile_id == id
        )
        await session.execute(query)
        await session.commit()
    elif dtype == "litter":
        query = delete(models.LitterEach).where(models.LitterEach.datafile_id == id)
        await session.execute(query)
        query = delete(models.LitterAnnual).where(models.LitterAnnual.datafile_id == id)
        await session.execute(query)
        await session.commit()
    elif dtype == "seed":
        query = delete(models.SeedEach).where(models.SeedEach.datafile_id == id)
        await session.execute(query)
        query = delete(models.SeedAnnual).where(models.SeedAnnual.datafile_id == id)
        await session.execute(query)
        await session.commit()
    else:
        pass
