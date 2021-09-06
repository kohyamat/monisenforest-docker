from typing import Optional

import numpy as np


def biomass(
    dbh: float,
    h: Optional[float] = None,
    wd: Optional[float] = None,
    ft: str = "DA",
    component: str = "agb",
    **kwargs,
) -> float:
    """
    Estimate tree biomass using the allometoric equation in Ishihara et al. 2015.

    Parameters
    ----------
    dbh: float
        diameter at brest height in cm
    h: float, optional
        tree height in cm
    wd: float, optional
        wood density in g/cm^3
    ft: str, default 'DA'
        functional type: 'DA', deciduous angiosperm, EA', evergreen angiosperm;
        'EG', evergreen gymnosperm
    component: str, default "agb"
        biomass component to estimate: 'agb', aboveground; 's', stem; 'b', branches;
        'l', leaves; 'r', roots

    """
    if h and np.isnan(h):
        h = None

    if wd and np.isnan(wd):
        wd = None

    if component == "agb":
        return biomass_agb(dbh, h=h, wd=wd, ft=ft)
    elif component == "s":
        return biomass_s(dbh, h=h, wd=wd, ft=ft)
    elif component == "b":
        return biomass_b(dbh, h=h, ft=ft)
    elif component == "l":
        return biomass_l(dbh, h=h, ft=ft)
    elif component == "r":
        return biomass_r(dbh, ft=ft)
    else:
        raise ValueError("Available value for componet are 'agb', 's', 'b', 'l', 'r'")


def biomass_agb(
    dbh: float,
    h: Optional[float] = None,
    wd: Optional[float] = None,
    ft: str = "DA",
    **kwargs,
) -> float:
    """
    Estimate above-ground biomass.

    Parameters
    ----------
    dbh: float
        diameter at brest height in cm
    h: float, optional
        tree height in cm
    wd: float, optional
        wood density in g/cm^3
    ft: str
        functional type: 'DA', deciduous angiosperm, EA', evergreen angiosperm;
        'EG', evergreen gymnosperm

    """
    if h and wd:
        x = np.array([1, np.log(dbh), np.log(h), np.log(wd)])
        coefs = np.array([-1.876, 2.174, 0.283, 0.611])
        return np.exp(np.inner(coefs, x))
    elif h:
        x = np.array([1, np.log(dbh), np.log(h)])
        coefs = {
            "DA": np.array([-2.407, 2.141, 0.390]),
            "EA": np.array([-2.230, 2.126, 0.347]),
            "EG": np.array([-2.356, 2.157, 0.247]),
        }
        return np.exp(np.inner(coefs[ft], x))
    elif wd:
        x = np.array([1, np.log(dbh), np.log(dbh) ** 2, np.log(dbh) ** 3, np.log(wd)])
        coefs = np.array([-1.196, 1.622, 0.338, -0.044, 0.708])
        return np.exp(np.inner(coefs, x))
    else:
        x = np.array([1, np.log(dbh), np.log(dbh) ** 2, np.log(dbh) ** 3])
        coefs = {
            "DA": np.array([-1.501, 1.375, 0.464, -0.061]),
            "EA": np.array([-1.698, 1.851, 0.239, -0.031]),
            "EG": np.array([-1.510, 1.157, 0.518, -0.067]),
        }
        return np.exp(np.inner(coefs[ft], x))


def biomass_s(
    dbh: float,
    h: Optional[float] = None,
    wd: Optional[float] = None,
    ft: str = "DA",
    **kwargs,
) -> float:
    """
    Estimate stem biomass.

    Parameters
    ----------
    dbh: float
        diameter at brest height in cm
    h: float, optional
        tree height in cm
    wd: float, optional
        wood density in g/cm^3
    ft: str
        functional type: 'DA', deciduous angiosperm, EA', evergreen angiosperm;
        'EG', evergreen gymnosperm

    """
    if h and wd:
        x = np.array([1, np.log(dbh), np.log(h), np.log(wd)])
        coefs = np.array([-2.589, 1.915, 0.728, 0.603])
        return np.exp(np.inner(coefs, x))
    elif h:
        x = np.array([1, np.log(dbh), np.log(h)])
        coefs = {
            "DA": np.array([-2.983, 1.907, 0.755]),
            "EA": np.array([-2.981, 1.880, 0.799]),
            "EG": np.array([-3.165, 1.810, 0.843]),
        }
        return np.exp(np.inner(coefs[ft], x))
    elif wd:
        x = np.array([1, np.log(dbh), np.log(dbh) ** 2, np.log(dbh) ** 3, np.log(wd)])
        coefs = np.array([-1.515, 1.647, 0.380, -0.056, 0.814])
        return np.exp(np.inner(coefs, x))
    else:
        x = np.array([1, np.log(dbh), np.log(dbh) ** 2, np.log(dbh) ** 3])
        coefs = {
            "DA": np.array([-1.867, 1.443, 0.487, -0.072]),
            "EA": np.array([-2.051, 1.810, 0.311, -0.047]),
            "EG": np.array([-2.056, 1.330, 0.492, -0.067]),
        }
        return np.exp(np.inner(coefs[ft], x))


def biomass_b(dbh: float, h: Optional[float] = None, ft: str = "DA", **kwargs) -> float:
    """
    Estimate branch biomass.

    Parameters
    ----------
    dbh: float
        diameter at brest height in cm
    h: float, optional
        tree height in cm
    ft: str
        functional type: 'DA', deciduous angiosperm, EA', evergreen angiosperm;
        'EG', evergreen gymnosperm

    """
    if h:
        x = np.array([1, np.log(dbh), np.log(h)])
        coefs = {
            "DA": np.array([-3.252, 3.113, -0.980]),
            "EA": np.array([-3.016, 3.085, -1.104]),
            "EG": np.array([-3.459, 3.105, -1.221]),
        }
        return np.exp(np.inner(coefs[ft], x))
    else:
        x = np.array([1, np.log(dbh)])
        coefs = {
            "DA": np.array([-4.134, 2.502]),
            "EA": np.array([-3.964, 2.400]),
            "EG": np.array([-4.189, 2.276]),
        }
        return np.exp(np.inner(coefs[ft], x))


def biomass_l(dbh: float, h: Optional[float] = None, ft: str = "DA", **kwargs) -> float:
    """
    Estimate leaf biomass.

    Parameters
    ----------
    dbh: float
        diameter at brest height in cm
    h: float, optional
        tree height in cm
    ft: str
        functional type: 'DA', deciduous angiosperm, EA', evergreen angiosperm;
        'EG', evergreen gymnosperm

    """
    if h:
        x = np.array([1, np.log(dbh), np.log(h)])
        coefs = {
            "DA": np.array([-4.306, 2.369, -0.541]),
            "EA": np.array([-3.230, 2.227, -0.718]),
            "EG": np.array([-3.162, 2.869, -1.253]),
        }
        return np.exp(np.inner(coefs[ft], x))
    else:
        x = np.array([1, np.log(dbh)])
        coefs = {
            "DA": np.array([-4.793, 2.031]),
            "EA": np.array([-3.850, 1.786]),
            "EG": np.array([-3.912, 2.018]),
        }
        return np.exp(np.inner(coefs[ft], x))


def biomass_r(dbh: float, ft: str = "DA", **kwargs) -> float:
    """
    Estimate root biomass.

    Parameters
    ----------
    dbh: float
        diameter at brest height in cm
    ft: str
        functional type: 'DA', deciduous angiosperm, EA', evergreen angiosperm;
        'EG', evergreen gymnosperm

    """
    x = np.array([1, np.log(dbh)])
    coefs = {
        "DA": np.array([-3.274, 2.315]),
        "EA": np.array([-3.432, 2.224]),
        "EG": np.array([-3.786, 2.345]),
    }
    return np.exp(np.inner(coefs[ft], x))
