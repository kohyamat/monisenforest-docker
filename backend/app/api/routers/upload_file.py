import hashlib
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List
import logging

import app.base as base
import app.summarise as summarise
from app.api.dependencies.database import get_crud
from app.crud import Crud
from app.schemas.plot import Plot, PlotCreate
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from starlette.status import HTTP_201_CREATED

router = APIRouter()



class DataExistsException(Exception):
    def __init__(self, id: int, data: Dict[Any, Any]):
        self.id = id
        self.data = data


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


@router.post(
    "/",
    response_model=Plot,
    name="upload_file:create_data_from_file",
    status_code=HTTP_201_CREATED,
)
async def upload_file(
    file: UploadFile = File(...),
    crud: Crud = Depends(get_crud(Crud)),
):
    tmppath = await save_upload_file_tmp(file)

    with tmppath.open("rb") as tmp:
        contents = tmp.read()
        md5 = hashlib.md5(contents).hexdigest()

    d = base.read_data(contents)
    date, name, name_jp = parse_metadata(d)

    new_plot = PlotCreate(
        plot_id=d.plot_id,
        name=name,
        name_jp=name_jp,
        filename=file.filename,
        md5=md5,
        dtype=d.data_type,
        date=date,
        size=round(sys.getsizeof(contents) / 1024, 1),
    )

    db_plot = await crud.get_plot_by_plotid_and_dtype(
        plot_id=new_plot.plot_id, dtype=new_plot.dtype
    )
    if db_plot:
        raise DataExistsException(
            id=db_plot.id, data={**new_plot.dict(), "tmppath": str(tmppath)}
        )
    else:
        tmppath.unlink()
        plot = await crud.create_plot(new_plot=new_plot)
        try:
            await create_data_summary(pid=plot.id, dtype=plot.dtype, d=d, crud=crud)
        except Exception as e:
            raise HTTPException(
                status_code=406,
                detail="Could not parse {}: {}".format(plot.filename, e),
            )
        finally:
            return plot


async def create_data_summary(
    pid: int,
    dtype: str,
    d: base.MonitoringData,
    crud: Crud,
) -> None:
    if dtype == "treeGBH":
        await create_tree_data(pid=pid, d=d, crud=crud)
    elif dtype == "litter":
        await create_litter_data(pid=pid, d=d, crud=crud)
    elif dtype == "seed":
        print("test")
        await create_seed_data(pid=pid, d=d, crud=crud)
    else:
        pass


async def create_tree_data(
    pid: int,
    d: base.MonitoringData,
    crud: Crud,
) -> None:
    ts = summarise.TreeSummary(d)
    query_values = [dict({"pid": pid}, **i) for i in ts.species_summary()]
    await crud.create_tree_sp_summary_many(query_values=query_values)

    query_values = [dict({"pid": pid}, **i) for i in ts.species_turnover()]
    await crud.create_tree_sp_turnover_many(query_values=query_values)

    query_values = [dict({"pid": pid}, **i) for i in ts.community_summary()]
    await crud.create_tree_com_summary_many(query_values=query_values)

    query_values = [dict({"pid": pid}, **i) for i in ts.community_turnover()]
    await crud.create_tree_com_turnover_many(query_values=query_values)


async def create_litter_data(
    pid: int,
    d: base.MonitoringData,
    crud: Crud,
):
    ls = summarise.LitterSummary(d)
    query_values = [dict({"pid": pid}, **i) for i in ls.each_sampling()]
    await crud.create_litter_each_many(query_values=query_values)

    query_values = [dict({"pid": pid}, **i) for i in ls.annual()]
    await crud.create_litter_annual_many(query_values=query_values)


async def create_seed_data(
    pid: int,
    d: base.MonitoringData,
    crud: Crud,
):
    ss = summarise.SeedSummary(d)
    query_values = [dict({"pid": pid}, **i) for i in ss.each_sampling()]
    await crud.create_seed_each_many(query_values=query_values)

    query_values = [dict({"pid": pid}, **i) for i in ss.annual()]
    await crud.create_seed_annual_many(query_values=query_values)


async def save_upload_file_tmp(file: UploadFile) -> Path:
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmppath = Path(tmp.name)
    finally:
        file.file.close()
    return tmppath
