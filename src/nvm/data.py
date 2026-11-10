"""Download der Rohdaten und Laden der aufbereiteten Panels."""

import os

import pandas as pd
import requests
from coinmetrics.api_client import CoinMetricsClient
from dotenv import load_dotenv

from nvm import config

load_dotenv(config.ROOT / ".env")


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


def load_raw(name: str) -> pd.DataFrame:
    """Liest eine Rohdatei (CSV) aus dem eingefrorenen Datenstand."""
    return pd.read_csv(config.SNAPSHOT_DIR / f"{name}.csv", index_col=0, parse_dates=True)


def load_panel(freq: str = "daily") -> pd.DataFrame:
    """Liest den Master-Datensatz (Panel 2012-01-01 bis 2026-06-30).

    Alle Analysen lesen nur hierüber:

    from nvm import data
    panel = data.load_panel("monthly")   # oder "daily"
    """
    paths = {"daily": config.PANEL_DAILY, "monthly": config.PANEL_MONTHLY}
    if freq not in paths:
        raise ValueError(f"freq muss 'daily' oder 'monthly' sein, nicht {freq!r}")
    if not paths[freq].exists():
        raise FileNotFoundError(
            f"{paths[freq]} fehlt. Erst bauen: uv run python scripts/02_build_panel.py"
        )
    return pd.read_parquet(paths[freq])
