# Datenquellen

Jede Datei in `data/raw/` steht hier mit Quelle, Abrufdatum und Skript, das sie erzeugt hat.
Rohdaten werden nach dem Download nie bearbeitet.

| Datei | Quelle | Inhalt | Abgerufen am | Von | Erzeugt durch |
|---|---|---|---|---|---|
| `data/raw/2026-11-15/coinmetrics_btc_daily.csv` | [Coin Metrics Community API](https://docs.coinmetrics.io/api/v4/) | PriceUSD, CapMrktCurUSD, CapMVRVCur, AdrActCnt, SplyCur, TxCnt (täglich) | _offen_ | _offen_ | `scripts/01_download.py` |
| `data/raw/2026-11-15/blockchain_com_estimated-transaction-volume-usd.csv` | [blockchain.com Charts API](https://www.blockchain.com/explorer/charts/estimated-transaction-volume-usd) | geschätztes On-chain-Transaktionsvolumen in USD (täglich) | _offen_ | _offen_ | `scripts/01_download.py` |

## Hinweise

- Realized Cap und das bereinigte Transaktionsvolumen (`CapRealUSD`, `TxTfrValAdjUSD`) sind in der
  Coin Metrics Community API nicht frei verfügbar. Realized Cap wird deshalb als
  `CapMrktCurUSD / CapMVRVCur` berechnet (`nvm.metrics.realized_cap`), das Volumen für NVT kommt
  von blockchain.com.
