import copy
import json
import re
from pathlib import Path
from typing import Any

import numpy as np

from app.base import MonitoringData
from app.datacheck import find_pattern, isvalid, retrive_year
from app.logger import get_logger

logger = get_logger(__name__)


fd = Path(__file__).resolve().parents[0]
path_spdict = fd.joinpath("suppl_data", "species_dict.json")
with open(path_spdict, "rb") as f:
    dict_sp = json.load(f)


def fill_after(x: np.ndarray, val: Any = 1, fill: Any = 2) -> np.ndarray:
    """
    Fill the elements after a specific value with a single value.

    Parameters
    ----------
    x : numpy ndarray
        One dimentional array
    val : any, default 1
        Value of the break point
    fill : any, default 2
        Value to use fill elements after the break point

    """
    x = np.array(x).copy()
    i = np.where(x == val)[0]
    if len(i) > 0:
        x[(i.min() + 1) :] = fill
    return x


def add_extra_columns_tree(d: MonitoringData) -> MonitoringData:
    """
    Add error/death/recruitment columns to a tree gbh data.

    毎木データに、エラー、死亡、加入の状態を表す列を追加。
    公開データに含まれるCSV2（*.transf.csv）。

    Parameters
    ----------
    d : MonitoringData
        MonitoringData object of tree gbh data

    """
    d = copy.deepcopy(d)
    gbh_mat, gbh_cn = d.select(regex="^gbh[0-9]{2}$", return_column_names=True)

    yrs = np.vectorize(retrive_year)(gbh_cn)
    yrs_order = np.argsort(yrs)

    gbh_mat = gbh_mat[:, yrs_order]
    gbh_cn = gbh_cn[yrs_order]
    yrs = yrs[yrs_order]
    gbh_mat_c = np.vectorize(
        lambda x: isvalid(x, "^nd|^cd|^vi|^vn", return_value=True)
    )(gbh_mat.copy())

    na_col = np.isnan(gbh_mat_c).all(axis=0)
    gbh_mat = gbh_mat[:, ~na_col]
    gbh_mat_c = gbh_mat_c[:, ~na_col]
    gbh_cn = gbh_cn[~na_col]
    yrs = yrs[~na_col]

    yrs_diff = np.diff(yrs)

    # Error
    error1 = np.where(np.vectorize(lambda x: find_pattern(x, "^nd"))(gbh_mat), 1, 0)
    error2 = np.where(
        np.vectorize(lambda x: find_pattern(x, "^cd|^vi|^vn"))(gbh_mat), 2, 0
    )
    error = (error1 + error2).astype(np.int64)

    # Dead
    pat_dxx = r"(?<![nd])d(?![d])\s?([0-9]+[.]?[0-9]*)"
    match_dxx = np.vectorize(lambda x: find_pattern(x, pat_dxx))(gbh_mat)
    for i, j in zip(*np.where(match_dxx)):
        if j > 0 and match_dxx[i, j - 1]:
            gbh_mat[i, j] = "na"
        else:
            gbh_mat[i, j] = "d"

    dead1 = np.where(
        np.vectorize(lambda x: find_pattern(x, "^(?<![nd])d(?![d])"))(gbh_mat), 1, 0
    )
    dead2 = np.where(np.vectorize(lambda x: find_pattern(x, "^dd"))(gbh_mat), 2, 0)
    dead = (dead1 + dead2).astype(np.int64)
    dead = np.apply_along_axis(lambda x: fill_after(x, 1, 2), 1, dead)

    # Recruit
    below_cutoff = np.vectorize(lambda x: np.less(x, 15.7, where=~np.isnan(x)))(
        gbh_mat_c
    )
    recr = np.zeros(gbh_mat_c.shape)

    # for first census
    not_recr_init = below_cutoff[:, 0] | np.isnan(gbh_mat_c[:, 0]) | (dead[:, 0] == 1)
    recr[:, 0][not_recr_init & (error[:, 0] == 0)] = -1

    change_state = np.apply_along_axis(np.diff, 1, np.isnan(gbh_mat_c) | below_cutoff)

    for i, j in zip(*np.where(change_state)):
        if np.isnan(gbh_mat_c[i, j + 1]):
            continue
        elif gbh_mat_c[i, j] > gbh_mat_c[i, j + 1]:
            continue
        elif len(np.where(recr[i, : (j + 1)] == 1)[0]) == 0:
            if (error[i, j] == 0) & (error[i, j + 1] == 0):
                if gbh_mat_c[i, j + 1] < (15.7 + 3.8 + yrs_diff[j] * 2.5):
                    recr[i, j + 1] = 1
                    recr[i, : (j + 1)] = -1
                elif not np.isnan(gbh_mat_c[i, j]):
                    recr[i, j + 1] = 1
                    recr[i, : (j + 1)] = -1
                elif len(np.where(recr[i, : (j + 1)] == -1)[0]) > 0:
                    recr[i, :j] = -1
            elif error[i, j] == 1:
                if len(np.where(recr[i, : (j + 1)] == -1)[0]) > 0:
                    recr[i, : np.where(error[i, : (j + 1)] == 1)[0][0]] = -1

    recr = recr.astype(np.int64)

    # 元の計測値を全て、nd等の記号を取り除いた数値のみのデータに置換
    # NOTE: np.nanが文字列の'nan'になるので注意
    d.data[0] = [re.sub("^(gbh[0-9]{2})$", r"\1_orig", i) for i in d.columns]

    # Add error, dead, recruit columns to data
    error_cn = [i.replace("gbh", "error") for i in gbh_cn]
    dead_cn = [i.replace("gbh", "dl") for i in gbh_cn]
    recr_cn = [i.replace("gbh", "rec") for i in gbh_cn]
    error = np.vstack((error_cn, error))
    dead = np.vstack((dead_cn, dead))
    recr = np.vstack((recr_cn, recr))
    gbh = np.vstack((gbh_cn, gbh_mat_c))

    d.data = np.hstack((d.data, gbh, error, dead, recr))
    return d


def add_taxon_info(
    d: MonitoringData, scientific_name: bool = True, classification: bool = False
) -> MonitoringData:
    """
    Add taxonomic information to tree-gbh/seed data.

    毎木/種子データに、種和名に基づいて分類学的情報を付加。

    Parameters
    ----------
    d : MonitoringData
        MonitoringData object of tree-gbh/seed data
    scientific_name : bool, default True
        If add scientific name
    classification : bool, default True
        If add classification
    """
    if d.data_type not in ["treeGBH", "seed"]:
        logger.warning("Input data is not tree data or seed data")
        return d

    global dict_sp

    class_cols = ["genus", "family", "order", "family_jp", "order_jp"]
    if scientific_name and classification:
        cols = ["species"] + class_cols
    elif scientific_name:
        cols = ["species"]
    elif classification:
        cols = class_cols
    else:
        logger.warning("No columns added.")
        return d

    add_cols = []
    not_found = []
    for i in d.select(regex="^spc_japan$|^spc$"):
        if i in dict_sp:
            add_cols.append([dict_sp[i][j] for j in cols])
        else:
            add_cols.append([""] * len(cols))
            if i not in not_found:
                not_found.append(i)

    if not_found:
        for i in not_found:
            msg = "{} not found in the species dictionary".format(i)
            logger.warning(msg)

    d.data = np.hstack((d.data, np.vstack((cols, add_cols))))
    return d
