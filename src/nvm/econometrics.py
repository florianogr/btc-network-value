"""Ökonometrische Bausteine: Einheitswurzeltests, Kointegration, VECM, Granger, OOS-R²."""

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, grangercausalitytests, kpss
from statsmodels.tsa.vector_ar.vecm import VECM, coint_johansen


def unit_root_table(df: pd.DataFrame) -> pd.DataFrame:
    """ADF (H0: Einheitswurzel) und KPSS (H0: Stationarität) für jede Spalte."""
    rows = {}
    for col in df.columns:
        x = df[col].dropna()
        adf_stat, adf_p, *_ = adfuller(x, autolag="AIC", result_object=False)
        kpss_stat, kpss_p, *_ = kpss(x, regression="c", nlags="auto", result_object=False)
        rows[col] = {
            "ADF": adf_stat,
            "ADF p": adf_p,
            "KPSS": kpss_stat,
            "KPSS p": kpss_p,
        }
    return pd.DataFrame(rows).T


def johansen(df: pd.DataFrame, det_order: int = 0, k_ar_diff: int = 1) -> pd.DataFrame:
    """Johansen-Trace-Test mit 5 %-kritischen Werten."""
    res = coint_johansen(df.dropna(), det_order, k_ar_diff)
    return pd.DataFrame(
        {"Trace": res.lr1, "5% krit.": res.cvt[:, 1]},
        index=[f"r <= {i}" for i in range(len(res.lr1))],
    )


def fit_vecm(df: pd.DataFrame, k_ar_diff: int = 1, coint_rank: int = 1, deterministic="ci"):
    """Schätzt ein VECM und gibt das statsmodels-Ergebnis zurück."""
    return VECM(
        df.dropna(), k_ar_diff=k_ar_diff, coint_rank=coint_rank, deterministic=deterministic
    ).fit()


def granger(df: pd.DataFrame, cause: str, effect: str, maxlag: int = 4) -> pd.DataFrame:
    """Granger-Kausalität von `cause` auf `effect` (F-Test je Lag)."""
    res = grangercausalitytests(df[[effect, cause]].dropna(), maxlag=maxlag, verbose=False)
    return pd.DataFrame(
        {lag: {"F": r[0]["ssr_ftest"][0], "p": r[0]["ssr_ftest"][1]} for lag, r in res.items()}
    ).T.rename_axis("Lag")


def oos_r2(actual: pd.Series, forecast: pd.Series, benchmark: pd.Series) -> float:
    """Out-of-sample-R² nach Campbell & Thompson (2008) gegen eine Benchmark-Prognose."""
    d = pd.concat({"a": actual, "f": forecast, "b": benchmark}, axis=1).dropna()
    return 1 - np.sum((d.a - d.f) ** 2) / np.sum((d.a - d.b) ** 2)
