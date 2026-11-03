"""Lädt alle Rohdaten in data/raw/<SNAPSHOT_DATE>/ (eingefrorener Datenstand).

    uv run python scripts/01_download.py                         # Datenstand einfrieren
    uv run python scripts/01_download.py data/local/test         # nur lokal ausprobieren

Läuft nicht in run_all.py. Bestehende Dateien werden nie überschrieben.
Nach dem Einfrieren SOURCES.md ergänzen.
"""

import sys
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from nvm import config, data


def save(target_dir: Path, name: str, fetch: Callable[[], pd.DataFrame | pd.Series]) -> bool:
    target = target_dir / f"{name}.csv"
    if target.exists():
        print(f"übersprungen  {name}: existiert schon")
        return True
    try:
        df = fetch()
    except Exception as e:
        print(f"FEHLER        {name}: {e}")
        return False
    df.to_csv(target)
    if isinstance(df.index, pd.DatetimeIndex):
        span = f"{df.index.min():%Y-%m-%d} bis {df.index.max():%Y-%m-%d}"
    else:
        span = f"{df.index[0]} bis {df.index[-1]}"
    print(f"ok            {name}: {len(df)} Zeilen, {span}")
    return True


def main() -> None:
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else config.SNAPSHOT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    jobs = {"coinmetrics_btc_daily": data.download_coinmetrics}
    for chart in config.BLOCKCHAIN_COM_CHARTS:
        jobs[f"blockchain_com_{chart}"] = lambda c=chart: data.download_blockchain_com(c)
    for series_id in config.FRED_SERIES:
        jobs[f"fred_{series_id}"] = lambda s=series_id: data.download_fred(s)
    for symbol, name in config.YAHOO_SYMBOLS.items():
        jobs[f"yahoo_{name}"] = lambda s=symbol: data.download_yahoo(s)
    jobs["farside_btc_etf_flows"] = data.download_farside_btc_etf_flows

    ok = [save(target_dir, name, fetch) for name, fetch in jobs.items()]
    print(f"\n{sum(ok)}/{len(ok)} Quellen -> {target_dir}")
    if not all(ok):
        sys.exit(1)


if __name__ == "__main__":
    main()
