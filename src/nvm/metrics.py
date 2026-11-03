"""Bewertungskennzahlen: Realized Cap, NVT, Stock-to-Flow, Metcalfe."""

import numpy as np
import pandas as pd


def nvt(market_cap: pd.Series, tx_volume: pd.Series, window: int = 90) -> pd.Series:
    """NVT-Signal: Marktkapitalisierung / gleitender Mittelwert des Transaktionsvolumens."""
    return market_cap / tx_volume.rolling(window).mean()


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
