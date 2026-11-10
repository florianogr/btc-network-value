"""Zentrale Konstanten. Zeiträume, Stichtage und Pfade werden NUR hier geändert.

Wer einen Wert ändert, macht das per Pull Request, damit alle drei Teile
mit demselben Stand rechnen.
"""

from pathlib import Path

import pandas as pd

# --- Pfade -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = ROOT / "output" / "figures"
TABLES_DIR = ROOT / "output" / "tables"

# --- Datenstand --------------------------------------------------------------
# Eingefrorener Download. Ordner data/raw/<SNAPSHOT_DATE>/ wird nie bearbeitet.
SNAPSHOT_DATE = "2026-11-03"
SNAPSHOT_DIR = RAW_DIR / SNAPSHOT_DATE

PANEL_DAILY = PROCESSED_DIR / "panel_daily.parquet"
PANEL_MONTHLY = PROCESSED_DIR / "panel_monthly.parquet"

# --- Stichprobe -------------------------------------------------------------
# Gemeinsam festgelegt am 10.11.2026. Nicht mehr ändern.
# Daten vor SAMPLE_START dienen nur als Vorlauf für gleitende Kennzahlen (NVT, S2F),
# sie fließen nicht in die Analyse ein.
SAMPLE_START = pd.Timestamp("2012-01-01")
SAMPLE_END = pd.Timestamp("2026-06-30")
OOS_START = pd.Timestamp("2020-01-01")  # Beginn der Out-of-sample-Phase

# --- Kennzahlen ---------------------------------------------------------------
# NVT Signal (Kalichkin 2018): Market Cap / gleitender Mittelwert des Transaktionsvolumens.
# Fehlen einzelne Tage, wird über die vorhandenen gemittelt, solange genug Tage da sind.
NVT_WINDOW = 90  # Hauptvariante
NVT_MIN_DAYS = 80
NVT_WINDOW_ROBUST = 365  # Robustheit: Jahresvolumen, analog zum Jahresgewinn im KGV
NVT_MIN_DAYS_ROBUST = 330

# --- Ereignisse -------------------------------------------------------------
HALVINGS = [
    pd.Timestamp("2012-11-28"),
    pd.Timestamp("2016-07-09"),
    pd.Timestamp("2020-05-11"),
    pd.Timestamp("2024-04-20"),
]
ETF_START = pd.Timestamp("2024-01-11")  # Handelsstart der US-Spot-ETFs

# --- Datenquellen -----------------------------------------------------------
ASSET = "btc"
# Welche Metrik woher kommt, steht in SOURCES.md.
# Coin Metrics Community API (frei). CapRealUSD und TxTfrValAdjUSD sind dort nicht frei:
# Realized Cap = CapMrktCurUSD / CapMVRVCur, Transaktionsvolumen kommt von blockchain.com.
COINMETRICS_METRICS = [
    "PriceUSD",  # Preis
    "CapMrktCurUSD",  # Marktkapitalisierung
    "CapMVRVCur",  # MVRV, daraus Realized Cap
    "AdrActCnt",  # aktive Adressen (für Metcalfe)
    "SplyCur",  # umlaufende Menge (für Stock-to-Flow)
    "TxCnt",  # Anzahl Transaktionen
    "IssTotNtv",  # neu geschürfte BTC pro Tag (Flow für Stock-to-Flow)
    "HashRate",  # Hashrate
]
# Rohdaten werden über die ganze verfügbare Historie geladen, die Stichprobe wählt 02_build_panel.
DOWNLOAD_START = pd.Timestamp("2009-01-03")

# blockchain.com Charts API (frei): geschätztes On-chain-Transaktionsvolumen in USD (für NVT)
BLOCKCHAIN_COM_CHARTS = ["estimated-transaction-volume-usd"]
