"""Lädt die Rohdaten EINMAL in data/raw/<SNAPSHOT_DATE>/.

Läuft nicht in run_all.py: der Datenstand ist eingefroren. Bestehende Dateien
werden nie überschrieben. Nach dem Download SOURCES.md ergänzen.
"""

import pandas as pd

from nvm import config, data


def save(df: pd.DataFrame | pd.Series, name: str) -> None:
    target = config.SNAPSHOT_DIR / f"{name}.csv"
    if target.exists():
        raise SystemExit(f"{target} existiert schon. Datenstand ist eingefroren.")
    df.to_csv(target)
    print(f"{name}: {len(df)} Zeilen, {df.index.min():%Y-%m-%d} bis {df.index.max():%Y-%m-%d}")


def main() -> None:
    config.SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    save(data.download_coinmetrics(), "coinmetrics_btc_daily")
    for chart in config.BLOCKCHAIN_COM_CHARTS:
        save(data.download_blockchain_com(chart), f"blockchain_com_{chart}")


if __name__ == "__main__":
    main()
