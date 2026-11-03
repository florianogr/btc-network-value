"""Download der Rohdaten und Laden der aufbereiteten Panels."""

import io
import os

import pandas as pd
import requests
from coinmetrics.api_client import CoinMetricsClient
from dotenv import load_dotenv

from nvm import config

load_dotenv(config.ROOT / ".env")

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)


def download_coinmetrics(
    metrics: list[str] = config.COINMETRICS_METRICS,
    start: pd.Timestamp = config.DOWNLOAD_START,
    end: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Lädt Tagesdaten für BTC von Coin Metrics (Community API, mit Key aus .env die Pro-API)."""
    client = CoinMetricsClient(api_key=os.getenv("COINMETRICS_API_KEY") or None)
    df = client.get_asset_metrics(
        assets=config.ASSET,
        metrics=metrics,
        start_time=start.strftime("%Y-%m-%d"),
        end_time=end.strftime("%Y-%m-%d") if end is not None else None,
        frequency="1d",
    ).to_dataframe()
    df["time"] = pd.to_datetime(df["time"]).dt.tz_localize(None).dt.normalize()
    return df.drop(columns="asset").set_index("time").sort_index()


def download_blockchain_com(chart: str) -> pd.Series:
    """Lädt eine Tagesreihe von der blockchain.com Charts API."""
    r = requests.get(
        f"https://api.blockchain.info/charts/{chart}",
        params={"timespan": "all", "format": "json", "sampled": "false"},
        timeout=60,
    )
    r.raise_for_status()
    values = pd.DataFrame(r.json()["values"])
    index = pd.to_datetime(values["x"], unit="s").dt.normalize().rename("time")
    return pd.Series(values["y"].to_numpy(), index=index, name=chart).sort_index()


def download_fred(series_id: str) -> pd.Series:
    """Lädt eine Tagesreihe von FRED (CSV-Export, kein API-Key nötig)."""
    r = requests.get(
        "https://fred.stlouisfed.org/graph/fredgraph.csv", params={"id": series_id}, timeout=90
    )
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text), index_col=0, parse_dates=True, na_values=".")
    return df.iloc[:, 0].rename(series_id).rename_axis("time")


def download_yahoo(symbol: str) -> pd.DataFrame:
    """Lädt Tageskurse (OHLC, Volumen, bereinigter Schlusskurs) von Yahoo Finance."""
    r = requests.get(
        f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}",
        params={"period1": 0, "period2": 4_000_000_000, "interval": "1d"},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=60,
    )
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    df = pd.DataFrame(res["indicators"]["quote"][0])
    if "adjclose" in res["indicators"]:
        df["adjclose"] = res["indicators"]["adjclose"][0]["adjclose"]
    df.index = pd.to_datetime(res["timestamp"], unit="s").normalize().rename("time")
    return df[["open", "high", "low", "close", "adjclose", "volume"]].sort_index()


def download_farside_btc_etf_flows() -> pd.DataFrame:
    """Lädt die Tabelle der täglichen Zuflüsse in US-Spot-Bitcoin-ETFs (Mio. USD) von Farside.

    Gespeichert wird die Tabelle wie veröffentlicht: Abflüsse in Klammern, "-" = kein Wert.
    """
    r = requests.get(
        "https://farside.co.uk/bitcoin-etf-flow-all-data/",
        headers={"User-Agent": BROWSER_UA},
        timeout=60,
    )
    r.raise_for_status()
    table = pd.read_html(io.StringIO(r.text))[0]
    table = table.dropna(subset=["Date"])
    return table[table["Date"] != "Total"].set_index("Date")


def load_raw(name: str) -> pd.DataFrame:
    """Liest eine Rohdatei (CSV) aus dem eingefrorenen Datenstand."""
    return pd.read_csv(config.SNAPSHOT_DIR / f"{name}.csv", index_col=0, parse_dates=True)


def load_panel(freq: str = "daily") -> pd.DataFrame:
    """Liest das aufbereitete Panel. Alle Analysen lesen nur hierüber."""
    path = {"daily": config.PANEL_DAILY, "monthly": config.PANEL_MONTHLY}[freq]
    return pd.read_parquet(path)
