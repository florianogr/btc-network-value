"""Bewertungskennzahlen: Realized Cap, NVT, Stock-to-Flow, Metcalfe."""

import numpy as np
import pandas as pd


def nvt(
    market_cap: pd.Series, tx_volume: pd.Series, window: int = 90, min_days: int | None = None
) -> pd.Series:
    """NVT-Signal: Marktkapitalisierung / gleitender Mittelwert des Transaktionsvolumens.

    Erwartet einen lückenlosen Tagesindex (fehlende Tage als NaN), weil das Fenster Zeilen zählt.
    Der Mittelwert wird über die vorhandenen Tage gebildet, wenn mindestens `min_days` da sind.
    """
    if not tx_volume.index.to_series().diff().dropna().eq(pd.Timedelta("1D")).all():
        raise ValueError("tx_volume braucht einen lückenlosen Tagesindex")
    return market_cap / tx_volume.rolling(window, min_periods=min_days or window).mean()


def stock_to_flow(supply: pd.Series, days: int = 365) -> pd.Series:
    """Bestand / jährlich neu geschürfte Menge (Tagesdaten)."""
    flow = supply.diff(days)
    return supply / flow


def metcalfe_value(active_addresses: pd.Series) -> pd.Series:
    """Metcalfe-Wert n² (Skalierungskonstante wird in der Regression geschätzt)."""
    return active_addresses.astype(float) ** 2


def realized_cap(market_cap: pd.Series, mvrv: pd.Series) -> pd.Series:
    """Realized Cap aus Marktkapitalisierung und MVRV (= Marktkapitalisierung / Realized Cap)."""
    return market_cap / mvrv


def log(series: pd.Series) -> pd.Series:
    """Natürlicher Logarithmus, nicht-positive Werte werden zu NaN."""
    return np.log(series.where(series > 0))
