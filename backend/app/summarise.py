import json
import re
from datetime import datetime
from operator import is_
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
from scipy import interpolate, optimize, special
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import OneHotEncoder

from app.allometry import biomass
from app.base import MonitoringData, read_data
from app.datacheck import (as_datetime, find_pattern, isvalid, retrive_year,
                           return_growth_year)
from app.utils import add_extra_columns_tree

fd = Path(__file__).resolve().parents[0]
path_spdict = fd.joinpath("suppl_data", "species_dict.json")
with open(path_spdict, "rb") as f:
    dict_sp = json.load(f)


def mask_invalid(arr: np.ndarray, pat_except: str = "^NA$|^na$|^nd|^-$"):
    """Mask invalid values."""
    arr_ = arr.copy()
    valid = np.vectorize(lambda x: isvalid(x, pat_except))(arr_)
    arr_[~valid] = np.nan
    arr_[arr_ == ""] = np.nan
    return arr_


def mean_date(x: Union[np.ndarray, List[datetime]], na_val: Any = None):
    x = np.array(x).copy()
    is_na = np.where(np.vectorize(is_)(x, na_val), True, False)
    x_min = x[~is_na].min()
    return x_min + (x[~is_na] - x_min).mean()


def fill_na_date_with_mean(x: np.ndarray, na_val: Any = None):
    x = np.array(x).copy()
    is_na = np.where(np.vectorize(is_)(x, na_val), True, False)
    x[is_na] = mean_date(x, na_val)
    return x


def binomln(n, k):
    """Calculate the natural logarithm of a binomial coefficient."""
    return -special.betaln(1 + n - k, 1 + k) - np.log(n + 1)


def period_mean(x1: float, x2: float):
    """Calculate period mean."""
    if x1 == x2:
        return x1
    else:
        return (x2 - x1) / np.log(x2 / x1)


def interpolate_gbh(
    gbh: np.ndarray, date: np.ndarray, err: np.ndarray, **kwargs
) -> np.ndarray:
    """
    Interpolate missing or errornous GBH values.

    Parameters
    ---------- gbh: numpy.ndarray
        1d array of GBH measurements
    date: numpy.ndarray
        1d array of survey dates in dtype of datetime.datetime
    err: numpy.ndarray
        1d array of intergers that indicates errors in measurements

    See Also
    --------
    scipy.interpolate.interp1d Interpolate a 1-D function.

    """
    gbh_interp = gbh.copy().astype("float64")
    if sum(err > 0) == 0:
        return gbh_interp
    elif sum(np.isfinite(gbh_interp[err == 0])) == 0:
        return gbh_interp

    is_alive = np.logical_or(np.isfinite(gbh_interp), err > 0)
    gbh_interp[err > 0] = np.nan
    date_int = np.array([int(i.astype("long")) for i in date.astype("datetime64")])
    x, y = date_int[is_alive], gbh_interp[is_alive]
    is_finite = np.isfinite(y)
    if len(y[is_finite]) > 1:
        # interpolate in logarithmic scale
        f = interpolate.interp1d(
            x[is_finite], np.log(y[is_finite]), fill_value="extrapolate", **kwargs
        )
        gbh_interp[is_alive] = np.exp(f(x))
    elif len(y[is_finite]) == 1:
        # repeat the same value if there is only one measurement
        gbh_interp[is_alive] = y[is_finite][0]

    return gbh_interp


def get_gbh(d, interpolate=True, spring_census=False):
    if d.select(regex="^error[0-9]{2}$").shape[1] == 0:
        d = add_extra_columns_tree(d)

    gbh_mat, gbh_cn = d.select(regex="^gbh[0-9]{2}$", return_column_names=True)
    # gbh_mat = gbh_mat.astype("float64")
    yrs = np.vectorize(retrive_year)(gbh_cn)
    yrs_order = np.argsort(yrs)
    gbh_mat = gbh_mat[:, yrs_order]
    gbh_cn = gbh_cn[yrs_order]
    gbh_mat = np.vectorize(lambda x: isvalid(x, return_value=True))(gbh_mat)
    na_col = np.isnan(gbh_mat).all(axis=0)
    gbh_mat = gbh_mat[:, ~na_col]
    gbh_cn = gbh_cn[~na_col]
    # err_mat = d.select(regex="^error[0-9]{2}$").astype("int")
    err_cn = [re.sub("gbh", "error", i) for i in gbh_cn]
    err_mat = d.select(err_cn).astype("int")
    date_cn = [re.sub("gbh", "s_date", i) for i in gbh_cn]
    try:
        date_mat = d.select(date_cn)
    except KeyError:
        date_mat = np.full(gbh_mat.shape, "")
    date_mat = np.vectorize(lambda x: as_datetime(x))(date_mat)

    if len(gbh_mat.shape) == 1:
        gbh_mat = gbh_mat[:, None]

    if len(err_mat.shape) == 1:
        err_mat = err_mat[:, None]

    if len(date_mat.shape) == 1:
        date_mat = date_mat[:, None]

    null_date = np.where(np.vectorize(is_)(date_mat, None), True, False)

    if np.all(null_date, axis=0).sum() > 0:
        # 調査日が全て不明の列がある場合は、その年の10月1日に調査したことにする
        # 春調査のサイトで調査日が欠損している場合は5月1日にする
        null_date_col = np.all(null_date, axis=0)
        years = [retrive_year(i) for i in gbh_cn]
        if spring_census:
            date_arr = [datetime.strptime("{}0501".format(i), "%Y%m%d") for i in years]
        else:
            date_arr = [datetime.strptime("{}1001".format(i), "%Y%m%d") for i in years]
        for j in np.where(null_date_col)[0]:
            date_mat[:, j] = date_arr[j]

    # GBHデータの欠損/エラー値の内挿・外挿
    if gbh_mat.shape[1] > 1 and interpolate:
        # 調査日の空白は同じ列の平均にする
        date_mat_ = np.apply_along_axis(
            lambda x: fill_na_date_with_mean(x, None), 0, date_mat
        )
        for i, (gbh, date, err) in enumerate(zip(gbh_mat, date_mat_, err_mat)):
            gbh_mat[i] = interpolate_gbh(gbh, date, err)

    return gbh_mat, date_mat


def est_agb(dbh_mat, sp_list):
    """
    Estimate above ground biomass using the allometric equation in Ishihara et al. 2015.
    """
    # wood density
    wd_list = [
        dict_sp[sp]["wood_density"]
        if sp in dict_sp and dict_sp[sp]["wood_density"]
        else None
        for sp in sp_list
    ]

    # functional type (生活形)
    # NOTE: 樹種不明の場合は最も頻度の高い生活形にする
    ft_categ = {1: "EG", 4: "DA", 5: "EA"}
    ft_list = [
        ft_categ[dict_sp[sp]["categ2"]]
        if sp in dict_sp and dict_sp[sp]["categ2"]
        else "NA"
        for sp in sp_list
    ]
    ft_u, ft_c = np.unique([i for i in ft_list], return_counts=True)
    ft_list = [ft_u[np.argmax(ft_c)] if i == "NA" else i for i in ft_list]

    w_mat = np.array(
        [
            np.vectorize(biomass)(dbh, wd=wd, ft=ft)
            for dbh, wd, ft in zip(dbh_mat, wd_list, ft_list)
        ]
    ).astype("float64")
    w_mat = w_mat / 1000  # kg to Mg

    return w_mat


def sp_sum(
    dbh_mat: np.ndarray,
    sp_list: np.ndarray,
    dbh_min: float = 5.0,
    w_mat: Optional[np.ndarray] = None,
    remove_sp_unknown: bool = True,
):
    """Calculate number of stems, basal area, biomass for each species."""
    sp_uniq, sp_labs = np.unique(sp_list, return_inverse=True)
    dbh_mat = dbh_mat.copy()
    if w_mat is None:
        w_mat = est_agb(dbh_mat, sp_list)
    else:
        w_mat = w_mat.copy()
    dbh_mat[np.isnan(dbh_mat)] = 0.0
    dbh_above = np.where(dbh_mat >= dbh_min, True, False)
    dbh_mat[~dbh_above] = 0.0
    w_mat[~dbh_above] = 0.0

    sp_n = np.apply_along_axis(lambda x: np.bincount(sp_labs, weights=x), 0, dbh_above)
    sp_ba = np.apply_along_axis(
        lambda x: np.bincount(sp_labs, weights=np.pi * (x / 100 / 2) ** 2), 0, dbh_mat
    )
    sp_b = np.apply_along_axis(lambda x: np.bincount(sp_labs, weights=x), 0, w_mat)

    if remove_sp_unknown:
        sp_unknown = np.array(
            [False if i in dict_sp and dict_sp[i]["species"] else True for i in sp_list]
        )
        sp_n = sp_n[np.unique(sp_labs[~sp_unknown]), :]
        sp_ba = sp_ba[np.unique(sp_labs[~sp_unknown]), :]
        sp_b = sp_b[np.unique(sp_labs[~sp_unknown]), :]
        sp_uniq = sp_uniq[np.unique(sp_labs[~sp_unknown])]

    return sp_n, sp_ba, sp_b, sp_uniq


def shannon_index(x):
    if len(x) > 1:
        x = x[x > 0]
        p = x / x.sum()
        return -sum(p * np.log(p))
    else:
        return 0.0


def rarefaction(n, sample):
    n_ = n.copy()
    n_min = n_.sum(axis=0).min()

    if sample > n_min:
        msg = "given re-sampling size is larger than smallest sample size"
        raise ValueError(msg)

    def f(x, sample):
        x = x[x > 0]
        x.min()
        tot = sum(x)
        lbinomc = binomln(tot, sample)
        lprob = np.array(
            [
                np.exp(binomln(tot - i, sample) - lbinomc) if (tot - i) > sample else 0
                for i in x
            ]
        )
        return float(sum(1 - lprob))

    return np.apply_along_axis(f, 0, n_, sample=sample)


def turnover_rates(
    dbh1: np.ndarray,
    dbh2: np.ndarray,
    w1: np.ndarray,
    w2: np.ndarray,
    t: Union[np.ndarray, float],
    plot_area: Optional[float] = None,
    dbh_min: float = 5.0,
):
    dbh1[np.isnan(dbh1)] = 0.0
    dbh2[np.isnan(dbh2)] = 0.0
    w1[np.isnan(w1)] = 0.0
    w2[np.isnan(w2)] = 0.0

    def _turnover(y: np.ndarray, z: np.ndarray, t: Union[np.ndarray, float]):
        if np.array_equal(y, z):
            return 0.0

        def f(x):
            return np.sum(y * np.exp(-x * t) - z)

        def fprime(x):
            return np.sum(-t * y * np.exp(-x * t))

        sol = optimize.root_scalar(f, x0=0.01, fprime=fprime, method="newton")
        return sol.root

    si = np.logical_and(dbh1 >= dbh_min, dbh2 >= dbh_min).astype("float64")
    di = np.logical_and(dbh1 >= dbh_min, dbh2 < dbh_min).astype("float64")
    ri = np.logical_and(dbh1 < dbh_min, dbh2 >= dbh_min).astype("float64")

    n_s0 = np.nansum(si)
    n_0 = n_s0 + np.nansum(di)
    n_t = n_s0 + np.nansum(ri)
    bs_0 = np.nansum(si * w1)
    bs_t = np.nansum(si * w2)
    b_0 = bs_0 + np.nansum(di * w1)
    b_t = bs_t + np.nansum(ri * w2)
    n_m = period_mean(n_0, n_t)
    b_m = period_mean(b_0, b_t)
    if plot_area:
        n_m = n_m / plot_area
        b_m = b_m / plot_area

    r_rel = _turnover(si + ri, si, t)
    m_rel = _turnover(si + di, si, t)
    p_rel = _turnover(w2, si * w1, t)
    l_rel = _turnover(w1, si * w1, t)

    return n_m, b_m, r_rel, m_rel, p_rel, l_rel


def group_median(x: np.ndarray, group_id: np.ndarray):
    unq = np.unique(group_id)

    if x.shape[0] != len(group_id):
        raise ValueError("lengths of the x and group_id should be the same")

    def f(x_):
        return np.array([np.nanmdeian(x_[group_id == i]) for i in unq])

    if len(x.shape) == 1:
        return f(x), unq
    elif len(x.shape) == 2:
        return np.apply_along_axis(f, 0, x), unq
    else:
        raise ValueError("x should be a one- or two-dimensional array")


def group_sum(x: np.ndarray, group_id: np.ndarray, remove_nan: bool = True):
    x = np.array(x)
    if len(x) != len(group_id):
        raise ValueError("lengths of the x and group_id should be the same")
    unq, idx, cnt = np.unique(group_id, return_inverse=True, return_counts=True)

    def f(x):
        if remove_nan:
            na = np.isnan(x)
            idx_unq = np.unique(idx)
            idx_unq_, idx_ = np.unique(idx[~na], return_inverse=True)
            res = np.repeat(np.nan, len(idx_unq))
            z = np.bincount(idx_, weights=x[~na])
            for i, j in zip(idx_unq_, z):
                res[i] = j
            return res
        else:
            return np.bincount(idx, weights=x)

    if len(x.shape) == 1:
        return f(x), unq
    elif len(x.shape) == 2:
        return np.apply_along_axis(f, 0, x), unq
    else:
        raise ValueError("x should be a one- or two-dimensional array")


def group_mean(x: np.ndarray, group_id: np.ndarray, remove_nan: bool = True):
    x = np.array(x)
    if len(x) != len(group_id):
        raise ValueError("lengths of the x and group_id should be the same")
    unq, idx, cnt = np.unique(group_id, return_inverse=True, return_counts=True)

    def f(x):
        if remove_nan:
            na = np.isnan(x)
            idx_unq = np.unique(idx)
            idx_unq_, idx_ = np.unique(idx[~na], return_inverse=True)
            res = np.repeat(np.nan, len(idx_unq))
            z = np.bincount(idx_, weights=x[~na]) / np.bincount(idx_)
            for i, j in zip(idx_unq_, z):
                res[i] = j
            return res
        else:
            return np.bincount(idx, weights=x) / np.bincount(idx)

    if len(x.shape) == 1:
        return f(x), unq
    elif len(x.shape) == 2:
        return np.apply_along_axis(f, 0, x), unq
    else:
        raise ValueError("x should be a one- or two-dimensional array")


class TreeSummary(object):

    _list_species_turnover: List[Dict[str, Union[str, float]]] = []

    def __init__(
        self, d: MonitoringData, dbh_min: float = 5.0, plot_area: Optional[float] = None
    ):
        self.d = d
        self.dbh_min = dbh_min
        self.plot_area = plot_area
        self.preprocessing()

    def preprocessing(self):
        if not self.plot_area:
            m = re.match(r"([0-9\.]*)\s?ha", self.d.metadata["PLOT SIZE"])
            if m:
                self.plot_area = float(m.group(1))
            else:
                self.plot_area = 1.0
                # raise ValueError("Plot area needed")

        self.sp_list = self.d.select(regex="^spc_japan$")

        if self.d.plot_id in ["OG-DB1", "UR-BC1"]:
            self.gbh_mat, self.date_mat = get_gbh(self.d, spring_census=True)
        else:
            self.gbh_mat, self.date_mat = get_gbh(self.d)

        # 初回調査で計測漏れが多い場合は除外
        if self.d.plot_id in ["GR-DB1", "TM-DB2"]:
            self.gbh_mat = self.gbh_mat[:, 1:]
            self.date_mat = self.date_mat[:, 1:]

        self.date_mat = self.date_mat.astype("datetime64[D]")
        # 樹木の成長年
        # 調査日が7月1日以前の場合、前年の成長分とする
        self.gyear_mat = np.vectorize(return_growth_year)(self.date_mat)
        # 成長年の空白は同じ列の平均で埋める
        self.gyear_mat = np.apply_along_axis(
            lambda x: fill_na_date_with_mean(x, na_val=-1), 0, self.gyear_mat
        )

        # remove empty column
        empty_col = np.where(np.isfinite(self.gbh_mat).sum(axis=0) == 0, True, False)
        self.gbh_mat = self.gbh_mat[:, ~empty_col]
        self.date_mat = self.date_mat[:, ~empty_col]
        self.gyear_mat = self.gyear_mat[:, ~empty_col]

        # GBH to DBH
        self.dbh_mat = self.gbh_mat / np.pi

        # biomass
        self.w_mat = est_agb(self.dbh_mat, self.sp_list)

        # above dbh threshold
        dbh_mat_ = self.dbh_mat.copy()
        dbh_mat_[np.isnan(dbh_mat_)] = 0.0
        self.dbh_above = np.where(dbh_mat_ >= self.dbh_min, True, False)

    def species_summary(self):
        sp_n, sp_ba, sp_b, sp_uniq = sp_sum(
            self.dbh_mat, self.sp_list, self.dbh_min, self.w_mat
        )
        t = self.gyear_mat.mean(axis=0)

        # remove species with no individuals with DBH >= 5 cm
        no_ind = np.where(sp_n.sum(axis=1) == 0, True, False)
        sp_n = sp_n[~no_ind, :]
        sp_ba = sp_ba[~no_ind, :]
        sp_b = sp_b[~no_ind, :]
        sp_uniq = sp_uniq[~no_ind]

        # sort by biomass
        sp_order = np.argsort(sp_b[:, -1])[::-1]
        sp_n = sp_n[sp_order, :]
        sp_ba = sp_ba[sp_order, :]
        sp_b = sp_b[sp_order, :]
        sp_uniq = sp_uniq[sp_order]

        # per area
        sp_n_area = sp_n / self.plot_area
        sp_ba_area = sp_ba / self.plot_area
        sp_b_area = sp_b / self.plot_area

        # proportion
        sp_n_prop = sp_n_area / sp_n_area.sum(axis=0) * 100
        sp_ba_prop = sp_ba_area / sp_ba_area.sum(axis=0) * 100
        sp_b_prop = sp_b_area / sp_b_area.sum(axis=0) * 100

        for i in range(sp_n.shape[0]):
            for j in range(sp_n.shape[1]):
                name_jp = sp_uniq[i]
                yield {
                    "year": t[j],
                    "species_jp": dict_sp[name_jp]["name_jp_std"],
                    "species": dict_sp[name_jp]["species"],
                    "family": dict_sp[name_jp]["family"],
                    "order": dict_sp[name_jp]["order"],
                    "n": sp_n_area[i, j],
                    "ba": sp_ba_area[i, j],
                    "b": sp_b_area[i, j],
                    "n_prop": sp_n_prop[i, j],
                    "ba_prop": sp_ba_prop[i, j],
                    "b_prop": sp_b_prop[i, j],
                }

    def _species_turnover(self):
        if self.dbh_mat.shape[1] == 1:
            return

        sp_uniq = np.unique(self.sp_list)
        si = np.logical_and(self.dbh_above[:, :-1], self.dbh_above[:, 1:]).astype(
            "float64"
        )
        t = self.gyear_mat.mean(axis=0)

        # 生存個体が5個体未満の種をOthersとしてまとめる
        rare_sp = np.array(
            [si[self.sp_list == i].sum(axis=0).min() < 5 for i in sp_uniq]
        )
        sp_list_ = self.sp_list.copy()
        sp_list_[np.array([i in sp_uniq[rare_sp] for i in sp_list_])] = "Others"

        # sort by biomass
        sp_b, sp_uniq = group_sum(self.w_mat[:, -1], sp_list_)
        if "Others" in sp_uniq:
            sp_order = np.argsort(sp_b[np.where(sp_uniq != "Others")])[::-1]
            sp_uniq = np.append(
                sp_uniq[np.where(sp_uniq != "Others")][sp_order], "Others"
            )
        else:
            sp_uniq = sp_uniq[np.argsort(sp_b)]

        # compute turnover rates for each species
        k = self.dbh_mat.shape[1]
        for sp in sp_uniq:
            for i, j in zip(range(k - 1), range(1, k)):
                res = turnover_rates(
                    self.dbh_mat[sp_list_ == sp, i],
                    self.dbh_mat[sp_list_ == sp, j],
                    self.w_mat[sp_list_ == sp, i],
                    self.w_mat[sp_list_ == sp, j],
                    np.diff(self.gyear_mat[sp_list_ == sp, i : (j + 1)]).flatten(),
                    plot_area=self.plot_area,
                )

                yield {
                    "t1": t[i],
                    "t2": t[j],
                    "species_jp": dict_sp[sp]["name_jp_std"]
                    if sp in dict_sp
                    else "その他",
                    "species": dict_sp[sp]["species"] if sp in dict_sp else "Others",
                    "family": dict_sp[sp]["family"] if sp in dict_sp else "",
                    "order": dict_sp[sp]["order"] if sp in dict_sp else "",
                    "n_m": res[0],
                    "b_m": res[1],
                    "r_rel": res[2],
                    "m_rel": res[3],
                    "p_rel": res[4],
                    "l_rel": res[5],
                    "r_abs": res[2] * res[0],
                    "m_abs": res[3] * res[0],
                    "p_abs": res[4] * res[1],
                    "l_abs": res[5] * res[1],
                }

    def species_turnover(self):
        if self._list_species_turnover:
            yield from self._list_species_turnover
        else:
            yield from self._species_turnover()

    def community_summary(self):
        sp_n, sp_ba, sp_b, sp_uniq = sp_sum(
            self.dbh_mat, self.sp_list, self.dbh_min, self.w_mat
        )

        # survey date
        mdate = np.apply_along_axis(lambda x: mean_date(x), 0, self.date_mat).astype(
            str
        )

        # year
        t = np.nanmean(self.gyear_mat, axis=0)

        # number of stems
        nstem = sp_n.sum(axis=0) / self.plot_area

        # number of species
        nsp = np.apply_along_axis(lambda x: sum(x > 0), 0, sp_n)

        # basal area
        ba = np.nansum((np.pi * (self.dbh_mat / 2) ** 2), 0) / 10000 / self.plot_area

        # biomass
        b = np.nansum(self.w_mat * self.dbh_above, 0) / self.plot_area

        # species richness
        richness = rarefaction(sp_n, sample=100)

        # species diversity
        shannon = np.apply_along_axis(shannon_index, 0, sp_n)

        keys = ["year", "mdate", "nstem", "nsp", "ba", "b", "richness", "shannon"]
        for values in zip(t, mdate, nstem, nsp, ba, b, richness, shannon):
            yield {k: v for k, v in zip(keys, values)}

    def community_turnover(self):
        # 種の幹数・現存量を重みとした、加重平均をプロット全体の変化速度とする
        if self.dbh_mat.shape[1] == 1:
            return

        if not self._list_species_turnover:
            self._list_species_turnover = list(self._species_turnover())

        x = np.array([list(i.values()) for i in self._list_species_turnover])
        t = x[:, :2].astype("float64")
        t_uniq = np.unique(t, axis=0)

        for t1, t2 in t_uniq:
            cond = np.logical_and(t[:, 0] == t1, t[:, 1] == t2)
            n_s, b_s, r_s, m_s, p_s, l_s = x[cond, 6:12].astype("float64").T

            r_rel = np.sum(np.array(r_s) * np.array(n_s)) / np.sum(n_s)
            m_rel = np.sum(np.array(m_s) * np.array(n_s)) / np.sum(n_s)
            p_rel = np.sum(np.array(p_s) * np.array(b_s)) / np.sum(b_s)
            l_rel = np.sum(np.array(l_s) * np.array(b_s)) / np.sum(b_s)
            n_m = np.sum(n_s)
            b_m = np.sum(b_s)
            r_abs = r_rel * n_m
            m_abs = m_rel * n_m
            p_abs = p_rel * b_m
            l_abs = l_rel * b_m

            yield {
                "t1": t1,
                "t2": t2,
                "n_m": n_m,
                "b_m": b_m,
                "r_rel": r_rel,
                "m_rel": m_rel,
                "p_rel": p_rel,
                "l_rel": l_rel,
                "r_abs": r_abs,
                "m_abs": m_abs,
                "p_abs": p_abs,
                "l_abs": l_abs,
            }


class LitterSummary(object):

    _list_each_sampling: List[Dict[str, Union[float, str]]] = []

    def __init__(self, d: MonitoringData):
        self.d = d
        self.preprocessing()
        self.impute()

    def preprocessing(self):
        pat_except = "^NA$|^na$|^nd|^-$"
        trap_area = self.d.select("trap_area").astype("float64")
        trap_id = self.d.select("trap_id")
        t1 = self.d.select("s_date1")
        t2 = self.d.select("s_date2")

        # get measurements of leaf, branch, rep
        meas = self.d.select(regex="^wdry_[lbr]|^w_[lbr]").copy()

        # mask invalid values
        meas = mask_invalid(meas, pat_except)

        # replace meas values below detection limit with the half of the lowest value
        meas_ = meas.copy()
        non_num = np.vectorize(lambda x: find_pattern(x, pat_except))(meas)
        meas_[non_num] = np.nan
        meas_ = meas_.astype("float64")
        meas_[np.where(meas_ < 0)] = 0
        dl = np.nanmin(meas_[meas_ != 0])
        meas[meas == "0"] = dl / 2

        # zero
        zero_val = np.vectorize(lambda x: find_pattern(x, "^-$"))(meas)
        meas[zero_val] = 0

        # nan
        nan_val = np.vectorize(lambda x: find_pattern(x, "^NA$|^na$|^nd"))(meas)
        meas[nan_val] = np.nan

        # nan from the description of the notes
        note = self.d.select("note")
        na_word = "倒れ|破損|裏返|斜|大破|破れ|転倒|ゴルフボール|ボール"
        na_word += "|食害|被害|穴|強風|積雪"
        na_match = np.array([True if re.search(na_word, x) else False for x in note])
        for x, na in zip(meas, na_match):
            if na:
                x[:] = np.nan

        # as float
        meas = meas.astype("float64")

        # fix negative values
        meas[meas < 0] = dl / 2

        # plot specific exceptions
        if self.d.plot_id == "IC-BC1":
            x = meas[(trap_id == "18") & (t1 == "20131029") & (t2 == "20131224")][0]
            meas[(trap_id == "18") & (t1 == "20131029") & (t2 == "20131127")] = x / 2
            meas[(trap_id == "18") & (t1 == "20131029") & (t2 == "20131224")] = x / 2
            t2[(trap_id == "18") & (t1 == "20131029") & (t2 == "20131224")] = "20131127"

        if self.d.plot_id == "OG-DB1":
            # 2005年-2006年は越冬設置？
            # 他の年と期間を揃えるために、s_date2を2005年末に
            t2[t2 == "20060315"] = "20051231"

        if self.d.plot_id == "OT-EC1":
            # 複数日に分けて回収した場合の日付を解析の都合上まとめる
            t1[t1 == "20110620"] = "20110617"
            t2[t2 == "20110620"] = "20110617"

        # convert unit
        meas = (meas.T / trap_area).T * 10 ** 4  # per ha
        meas = meas / 10 ** 6  # to Mg

        # exclude rows where all measurements are nan
        na_row = np.isnan(meas).all(axis=1)
        self.wdry = meas[~na_row, :3]
        self.w = meas[~na_row, 3:]
        self.t1 = t1[~na_row]
        self.t2 = t2[~na_row]

    def impute(self):
        # impute missing data
        if self.d.plot_id == "OG-DB1":
            # 小川のデータで一部風乾重から絶乾重への変換がされていない箇所を補完
            X_rep = np.c_[self.wdry[:, 2], self.w[:, 2]]
            cond = np.where(np.isnan(X_rep).sum(axis=1) != 2, True, False)
            imputer = IterativeImputer(max_iter=10, random_state=0)
            X_rep_impute = imputer.fit_transform(X_rep[cond, :])
            self.wdry[cond, 2] = X_rep_impute[:, 0]
            self.w[cond, 2] = X_rep_impute[:, 1]

    def _each_sampling(self):
        # calculate mean for each sampling
        t1 = np.array([as_datetime(i) for i in self.t1]).astype("datetime64[D]")
        t2 = np.array([as_datetime(i) for i in self.t2]).astype("datetime64[D]")
        tm = t1 + (t2 - t1) / 2
        t = np.c_[t1, t2]
        t_uniq = np.unique(t, axis=0)

        wdry_m, tm_uniq = group_mean(self.wdry, tm)
        wdry_all = np.nansum(wdry_m, axis=1)
        wdry_m = np.vstack((wdry_m.T, wdry_all)).T

        inst_period = np.diff(t_uniq).flatten().astype(int)
        year = tm_uniq.astype("datetime64[Y]").astype(str).astype(int)
        for i in range(len(wdry_m)):
            yield {
                "year": year[i],
                "t1": t_uniq[i, 0].astype(str),
                "t2": t_uniq[i, 1].astype(str),
                "inst_period": inst_period[i],
                "wdry_leaf": wdry_m[i, 0],
                "wdry_branch": wdry_m[i, 1],
                "wdry_rep": wdry_m[i, 2],
                "wdry_all": wdry_m[i, 3],
            }

    def each_sampling(self):
        if self._list_each_sampling:
            yield from self._list_each_sampling
        else:
            yield from self._each_sampling()

    def annual(self, exclude_low_sampling_density: bool = True):
        if not self._list_each_sampling:
            self._list_each_sampling = list(self._each_sampling())

        x = np.array([list(i.values()) for i in self._list_each_sampling])

        # 1/1-12/31で集計
        # 年をまたぐ場合は日割りで計算
        t = x[:, 1:3].astype("datetime64[D]")
        t_year = t.astype("datetime64[Y]").astype(str).astype(int)
        inst_period_raw = x[:, 3].astype(int)
        year = np.unique(t_year)
        wdry_raw = x[:, 4:8].astype("float64")
        wdry_daily = (wdry_raw.T / inst_period_raw).T

        exclude_low_sampling_density = True

        wdry_cum = np.empty(shape=(0, wdry_raw.shape[1]))
        n_collect = np.array([])
        inst_period = np.array([])
        t1 = np.array([])
        t2 = np.array([])

        for yr in year:
            m = np.any(t_year == yr, axis=1)
            t_s = t[m]
            yr_diff = t_year[m] - yr
            t_s[np.where(yr_diff == -1)] = "{}-12-31".format(yr - 1)
            t_s[np.where(yr_diff == 1)] = "{}-12-31".format(yr)
            wdry_daily_s = wdry_daily[m]
            wdry_cum_s = np.nansum(wdry_daily_s * np.diff(t_s).astype(int), axis=0)
            wdry_cum = np.vstack((wdry_cum, wdry_cum_s))
            n_collect = np.append(n_collect, np.sum(np.all(yr_diff != 1, axis=1)))
            inst_period = np.append(inst_period, np.diff(t_s).astype(int).sum())
            t1 = np.append(t1, t_s[0, 0].astype(str))
            t2 = np.append(t2, t_s[-1, 1].astype(str))

        # 設置期間およびリター回収回数が例年の75%に満たない年は除外
        if exclude_low_sampling_density:
            low = np.logical_and(
                inst_period < (np.median(inst_period) * 0.75),
                n_collect < (np.median(n_collect) * 0.75),
            )
            inst_period = inst_period[~low]
            year = year[~low]
            wdry_cum = wdry_cum[~low]
            n_collect = n_collect[~low]
            t1 = t1[~low]
            t2 = t2[~low]

        for i in range(len(wdry_cum)):
            yield {
                "year": year[i],
                "t1": t1[i],
                "t2": t2[i],
                "inst_period": inst_period[i],
                "n_collect": int(n_collect[i]),
                "wdry_leaf": wdry_cum[i, 0],
                "wdry_branch": wdry_cum[i, 1],
                "wdry_rep": wdry_cum[i, 2],
                "wdry_all": wdry_cum[i, 3],
            }


def fix_seed_data_AM(d: MonitoringData):
    form_col = d.columns.tolist().index("form")
    number_col = d.columns.tolist().index("number")

    match_idx = []
    for i, v in enumerate(d.values):
        f = v[form_col]
        sn = re.search("種子([0-9])+", f)
        fn = re.search("果実([0-9])+", f)
        cn = re.search("[殻柄皮]([0-9])+", f)
        if any([sn, fn, cn]):
            match_idx.append(i)
    not_match_idx = [i for i in range(d.values.shape[0]) if i not in match_idx]

    s1 = d.values.copy()[np.array(match_idx), :]
    s2 = d.values.copy()[np.array(not_match_idx), :]

    s1_new = np.empty(shape=(0, d.values.shape[1]))
    for i, v in enumerate(s1):
        f = v[form_col]
        sn = re.search("種子([0-9])+", f)
        fn = re.search("果実([0-9])+", f)
        cn = re.search("[殻柄皮]([0-9])+", f)
        if fn:
            vf = v.copy()
            vf[number_col] = fn.group(1)
            vf[form_col] = "果実"
            s1_new = np.vstack((s1_new, vf))
        if sn:
            vs = v.copy()
            vs[number_col] = sn.group(1)
            vs[form_col] = "種子"
            s1_new = np.vstack((s1_new, vs))
        if cn:
            vc = v.copy()
            vc[number_col] = cn.group(1)
            vc[form_col] = "殻柄"
            s1_new = np.vstack((s1_new, vc))

    d.data = np.vstack((d.columns, s1_new, s2))
    return d


def impute_seed_meas(
    number: np.ndarray, wdry: np.ndarray, form: np.ndarray, status: np.ndarray
):
    enc = OneHotEncoder()
    dummies = enc.fit_transform(np.c_[status, form]).toarray()
    X = np.c_[number, wdry, dummies]
    imputer = IterativeImputer(max_iter=10, random_state=0)
    X_impute = imputer.fit_transform(X)
    return X_impute[:, 0], X_impute[:, 1]


class SeedSummary(object):

    _list_each_sampling: List[Dict[str, Union[float, str]]] = []

    def __init__(self, d: MonitoringData):
        self.d = d
        self.preprocessing()
        self.impute()

    def preprocessing(self):
        pat_except = "^NA$|^na$|^nd|^-$"

        if self.d.plot_id == "AM-EB1":
            self.d.values[:, self.d.columns == "trap_area"] = "0.5"
            self.d = fix_seed_data_AM(self.d)

        trap_area = self.d.select("trap_area").astype("float64")
        t1 = self.d.select("s_date1")
        t2 = self.d.select("s_date2")
        sp_list = np.array(
            [
                dict_sp[i]["name_jp_std"] if i in dict_sp else ""
                for i in self.d.select(regex="^spc$")
            ]
        )

        # get measurements
        number = self.d.select(regex="^number$").copy()
        wdry = self.d.select(regex="^wdry$").copy()

        if self.d.plot_id == "OG-DB1":
            # 小川は2017以前は風乾重で、それ以降は絶乾重
            wdry = self.d.select(regex="^wdry$|^w$").copy()

        # mask invalid values
        number = mask_invalid(number)
        wdry = mask_invalid(wdry)

        # replace wdry values below detection limit with the half of the lowest value
        wdry_ = wdry.copy()
        non_num = np.vectorize(lambda x: find_pattern(x, pat_except))(wdry)
        wdry_[non_num] = np.nan
        wdry_ = wdry_.astype("float64")
        wdry_[np.where(wdry_ < 0)] = 0
        dl = np.nanmin(wdry_[wdry_ != 0])
        wdry[wdry == "0"] = dl / 2

        # zero
        zero_val = np.vectorize(lambda x: find_pattern(x, "^-$"))(number)
        number[zero_val] = 0
        zero_val = np.vectorize(lambda x: find_pattern(x, "^-$"))(wdry)
        wdry[zero_val] = 0

        # nan
        nan_val = np.vectorize(lambda x: find_pattern(x, "^NA$|^na$|^nd"))(number)
        number[nan_val] = np.nan
        nan_val = np.vectorize(lambda x: find_pattern(x, "^NA$|^na$|^nd"))(wdry)
        wdry[nan_val] = np.nan

        # as float
        wdry = wdry.astype("float64")
        number = number.astype("float64")

        if self.d.plot_id == "OG-DB1":
            wdry = np.nansum(wdry, axis=1)

        # fix negative values
        wdry[wdry < 0] = np.nan
        number[number < 0] = np.nan

        # Replace 0 with nan if one of the measurements is 0 and
        # the other is greater than 0.
        wdry[(wdry == 0) & (number > 0)] = np.nan
        number[(wdry > 0) & (number == 0)] = np.nan

        # convert unit
        wdry = wdry / trap_area  # g per m^2
        number = number / trap_area  # per m^2

        # plot specific exceptions
        trap_id = self.d.select("trap_id")
        if self.d.plot_id == "IC-BC1":
            x = wdry[(trap_id == "18") & (t1 == "20131029") & (t2 == "20131224")][0]
            wdry[(trap_id == "18") & (t1 == "20131029") & (t2 == "20131127")] = x / 2
            wdry[(trap_id == "18") & (t1 == "20131029") & (t2 == "20131224")] = x / 2
            t2[(trap_id == "18") & (t1 == "20131029") & (t2 == "20131224")] = "20131127"

        if self.d.plot_id == "OG-DB1":
            # 2005年-2006年は越冬設置？
            # 他の年と期間を揃えるために、s_date2を2005年末に
            t2[t2 == "20060315"] = "20051231"

        if self.d.plot_id == "OT-EC1":
            # 複数日に分けて回収した場合の日付を解析の都合上まとめる
            t1[t1 == "20110620"] = "20110617"
            t2[t2 == "20110620"] = "20110617"

        # status
        status_good = re.compile("^健全$|^充実$|^見た目健全$")
        status_na = re.compile("^区別[無な]し$|^未分類$|^不明$|^-$|^NA$|^nd$")
        status = np.array(
            [
                "good"
                if status_good.match(i.strip())
                else "na"
                if status_na.match(i.strip())
                else "bad"
                for i in self.d.select("status")
            ]
        )

        # form
        form_fruit = re.compile("果|実")
        form_seed = re.compile("種子")
        form_na = re.compile("区別[な無]し|^NA$|^nd$|^-$")
        form = np.array(
            [
                "fruit"
                if form_fruit.match(i.strip())
                else "seed"
                if form_seed.match(i.strip())
                else "na"
                if form_na.match(i.strip())
                else "other"
                for i in self.d.select("form")
            ]
        )

        # exclude rows
        na_row = np.isnan(np.c_[wdry, number]).all(axis=1)
        sp_unknown = np.where(sp_list == "", True, False)
        form_other = np.where(form == "ohter", True, False)
        self.wdry = wdry[~(na_row | sp_unknown | form_other)]
        self.number = number[~(na_row | sp_unknown | form_other)]
        self.t1 = t1[~(na_row | sp_unknown | form_other)]
        self.t2 = t2[~(na_row | sp_unknown | form_other)]
        self.form = form[~(na_row | sp_unknown | form_other)]
        self.status = status[~(na_row | sp_unknown | form_other)]
        self.trap_area = trap_area[~(na_row | sp_unknown | form_other)]
        self.sp_list = sp_list[~(na_row | sp_unknown | form_other)]

    def impute(self):
        # impute missing data
        if self.d.plot_id not in ["OG-DB1", "AM-EB1"]:
            for s in np.unique(self.sp_list):
                cond = np.where(self.sp_list == s, True, False)
                if np.all(np.isnan(self.number[cond])) | np.all(
                    np.isnan(self.wdry[cond])
                ):
                    continue

                if np.any(np.isnan(self.number[cond]) & np.isnan(self.wdry[cond])):
                    number_imp, wdry_imp = impute_seed_meas(
                        self.number[cond],
                        self.wdry[cond],
                        self.form[cond],
                        self.status[cond],
                    )
                    self.number[cond] = number_imp
                    self.wdry[cond] = wdry_imp

        elif self.d.plot_id == "OG-DB1":
            # 小川では2008年以降は重量がstatus別になっておらず、まとめて計量されている
            # それ以前のデータについて補完する
            t2 = np.array([as_datetime(i) for i in self.t2]).astype("datetime64[D]")
            t_ = np.where(t2 <= np.datetime64("2007-11-18"), True, False)

            for s in np.unique(self.sp_list[t_]):
                cond = np.where((self.sp_list == s) & t_, True, False)
                if np.all(np.isnan(self.number[cond])) | np.all(
                    np.isnan(self.wdry[cond])
                ):
                    continue

                if np.any(np.isnan(self.number[cond]) & np.isnan(self.wdry[cond])):
                    number_imp, wdry_imp = impute_seed_meas(
                        self.number[cond],
                        self.wdry[cond],
                        self.form[cond],
                        self.status[cond],
                    )
                    self.number[cond] = number_imp
                    self.wdry[cond] = wdry_imp

        elif self.d.plot_id == "AM-EB1":
            # 奄美はスダジイのみ補完
            # それ以外の種は回収時毎にまとめて計量されている
            cond = np.where(self.sp_list == "スダジイ", True, False)
            number_imp, wdry_imp = impute_seed_meas(
                self.number[cond],
                self.wdry[cond],
                self.form[cond],
                self.status[cond],
            )
            self.number[cond] = number_imp
            self.wdry[cond] = wdry_imp

    def _each_sampling(self):
        # calculate mean by species and sampling
        t1 = np.array([as_datetime(i) for i in self.t1]).astype("datetime64[D]")
        t2 = np.array([as_datetime(i) for i in self.t2]).astype("datetime64[D]")
        tm = t1 + (t2 - t1) / 2
        tm_uniq = np.unique(tm)
        t = np.c_[t1, t2]
        t_uniq = np.unique(t, axis=0)

        sp_uniq, cnt = np.unique(self.sp_list, return_counts=True)
        sp_uniq = sp_uniq[cnt > 9]
        sp_tm_combn = np.array([i + ":" + str(j) for i, j in zip(self.sp_list, tm)])
        sp_tm_combn_all = np.array(
            [[i + ":" + str(j) for j in tm_uniq] for i in sp_uniq]
        ).flatten()

        sp_list, tm_arr = np.array([i.split(":") for i in sp_tm_combn_all]).T
        tm_arr = tm_arr.astype("datetime64[D]")
        year = tm_arr.astype("datetime64[Y]").astype(str).astype(int)

        X = np.c_[self.number, self.wdry]
        X_sum, sp_tm_combn_uniq = group_sum(X, sp_tm_combn)

        number_sum = np.array(
            [
                X_sum[sp_tm_combn_uniq == i, 0][0] if i in sp_tm_combn_uniq else 0
                for i in sp_tm_combn_all
            ]
        )
        wdry_sum = np.array(
            [
                X_sum[sp_tm_combn_uniq == i, 1][0] if i in sp_tm_combn_uniq else 0
                for i in sp_tm_combn_all
            ]
        )

        if self.d.plot_id == "KM-DB1":
            # カヌマ沢のトラップ数は2004, 2005年が60で、それ以降は25
            n_trap = np.where(year < 2006, 60, 25)
        else:
            n_trap = int(re.sub(r"^([0-9]+).*", r"\1", self.d.metadata["NO. OF TRAPS"]))

        number_m = number_sum / n_trap
        wdry_m = wdry_sum / n_trap

        # calculate the proprtion of healthy seeds
        enc = OneHotEncoder()
        enc.fit(self.status[:, None])
        cat = enc.categories_[0]
        if "good" in cat:
            dummies = (
                enc.fit_transform(self.status[:, None]).toarray() * self.number[:, None]
            )
            status_sum, _ = group_sum(dummies, sp_tm_combn)
            prop_status = np.array(
                [
                    i / i.sum() if i.sum() > 0 else np.repeat(np.nan, len(cat))
                    for i in status_sum
                ]
            )
            prop_viable = prop_status[:, cat == "good"].flatten()
            if "na" in cat:
                prop_viable[prop_status[:, cat == "na"].flatten() == 1] = np.nan

            prop_viable = np.array(
                [
                    prop_viable[np.where(sp_tm_combn_uniq == i)[0][0]]
                    if i in sp_tm_combn_uniq
                    else np.nan
                    for i in sp_tm_combn_all
                ]
            )
        else:
            prop_viable = np.repeat(np.nan, len(number_m))

        # sort by dry mass
        sp_wdry_sum = {k: v for v, k in zip(*group_sum(wdry_m, sp_list))}
        order = np.lexsort((-np.array([sp_wdry_sum[i] for i in sp_list]), year))
        wdry_m = wdry_m[order]
        number_m = number_m[order]
        prop_viable = prop_viable[order]
        sp_list = sp_list[order]
        year = year[order]
        tm_arr = tm_arr[order]

        # rounding
        wdry_m = np.round(wdry_m, 8)
        number_m = np.round(number_m, 8)
        prop_viable = np.round(prop_viable, 8)

        for i in range(len(number_m)):
            j = np.where(tm_uniq == tm_arr[i])[0][0]
            yield {
                "year": year[i],
                "t1": t_uniq[j, 0].astype(str),
                "t2": t_uniq[j, 1].astype(str),
                "inst_period": np.diff(t_uniq[j]).astype(int)[0],
                "species_jp": sp_list[i],
                "species": dict_sp[sp_list[i]]["species"],
                "family": dict_sp[sp_list[i]]["family"],
                "order": dict_sp[sp_list[i]]["order"],
                "number": number_m[i],
                "wdry": wdry_m[i],
                "prop_viable": prop_viable[i],
            }

    def each_sampling(self):
        if self._list_each_sampling:
            yield from self._list_each_sampling
        else:
            yield from self._each_sampling()

    def annual(self, exclude_short_inst_period: bool = False):
        if not self._list_each_sampling:
            self._list_each_sampling = list(self._each_sampling())

        x = np.array([list(i.values()) for i in self._list_each_sampling])

        year = x[:, 0].astype(int)
        inst_period = x[:, 3].astype(int)
        sp = x[:, 4]
        number = x[:, 8].astype("float64")
        wdry = x[:, 9].astype("float64")
        prop_viable = x[:, 10].astype("float64")

        sp_year = np.array([i + ":" + str(j) for i, j in zip(sp, year)])
        inst_period_sum, sp_year_uniq = group_sum(inst_period, sp_year)
        number_sum, _ = group_sum(number, sp_year)
        wdry_sum, _ = group_sum(wdry, sp_year)
        sp_list, year_list = np.array([i.split(":") for i in sp_year_uniq]).T
        year_list = year_list.astype(int)

        prop_viable_sum = np.array([])
        for i in sp_year_uniq:
            wdry[sp_year == i]
            n = number[sp_year == i]
            p = prop_viable[sp_year == i]
            if any(np.isfinite(n)) and np.any(np.isfinite(p)):
                p_ = np.nansum(n * p) / np.nansum(n)
            else:
                p_ = np.nan
            prop_viable_sum = np.append(prop_viable_sum, p_)

        if exclude_short_inst_period:
            short = np.where(
                inst_period_sum < (np.median(inst_period_sum) * 0.8), True, False
            )
            inst_period_sum = inst_period_sum[~short]
            year_list = year_list[~short]
            sp_list = sp_list[~short]
            wdry_sum = wdry_sum[~short]
            number_sum = number_sum[~short]
            prop_viable_sum = prop_viable_sum[~short]

        t1 = np.array(
            [x[year == i, 1].astype("datetime64[D]").min() for i in year_list]
        ).astype("str")

        t2 = np.array(
            [x[year == i, 2].astype("datetime64[D]").max() for i in year_list]
        ).astype("str")

        # sort by dry mass
        sp_wdry_sum = {k: v for v, k in zip(*group_sum(wdry_sum, sp_list))}
        order = np.lexsort((-np.array([sp_wdry_sum[i] for i in sp_list]), year_list))

        wdry_sum = wdry_sum[order]
        number_sum = number_sum[order]
        prop_viable_sum = prop_viable_sum[order]
        sp_list = sp_list[order]
        year_list = year_list[order]
        inst_period_sum = inst_period_sum[order]
        t1 = t1[order]
        t2 = t2[order]

        # rounding
        wdry_sum = np.round(wdry_sum, 8)
        number_sum = np.round(number_sum, 8)
        prop_viable_sum = np.round(prop_viable_sum, 8)

        for i in range(len(wdry_sum)):
            yield {
                "year": year_list[i],
                "t1": t1[i],
                "t2": t2[i],
                "inst_period": inst_period_sum[i],
                "species_jp": sp_list[i],
                "species": dict_sp[sp_list[i]]["species"],
                "family": dict_sp[sp_list[i]]["family"],
                "order": dict_sp[sp_list[i]]["order"],
                "number": number_sum[i],
                "wdry": wdry_sum[i],
                "prop_viable": prop_viable_sum[i],
            }


if __name__ == "__main__":
    import time
    from pathlib import Path

    dd = read_data("./data/Tree/AI-BC1-TreeGbh-2004-2020-ver2.xlsx")
    obj1 = TreeSummary(dd)
    for i in obj1.species_turnover():
        print(i)

    # dd = read_data("./data/Litter/TM-DB1-Litter-2004-2019-ver2.xlsx")
    # obj2 = LitterSummary(dd)
    # for i in obj2.annual():
    #     print(i)

    dd = read_data("./data/Seed/AI-BC1-Seed-2004-2019-ver1.xlsx")
    obj3 = SeedSummary(dd)
    for i in obj3.annual():
        print(i)
