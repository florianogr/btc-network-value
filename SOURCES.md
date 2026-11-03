# Datenquellen

Jede Datei in `data/raw/` steht hier mit Quelle, Abrufdatum und Skript, das sie erzeugt hat.
Rohdaten werden nach dem Download nie bearbeitet. Alle Dateien erzeugt `scripts/01_download.py`.

Datenstand: `data/raw/2026-11-03/` · abgerufen am 03.11.2026 · von Florian

| Datei | Quelle | Inhalt | Verfügbar ab |
|---|---|---|---|
| `coinmetrics_btc_daily.csv` | [Coin Metrics Community API](https://docs.coinmetrics.io/api/v4/) | PriceUSD, CapMrktCurUSD, CapMVRVCur, AdrActCnt, SplyCur, TxCnt, IssTotNtv, HashRate | 2009-01-03 (Preis ab 2010-07-18) |
| `blockchain_com_estimated-transaction-volume-usd.csv` | [blockchain.com Charts API](https://www.blockchain.com/explorer/charts/estimated-transaction-volume-usd) | geschätztes On-chain-Transaktionsvolumen in USD | 2010-08-28 |
| `fred_SP500.csv` | [FRED](https://fred.stlouisfed.org/series/SP500) | S&P 500 (FRED liefert nur 10 Jahre) | 2016-11 |
| `fred_NASDAQCOM.csv` | [FRED](https://fred.stlouisfed.org/series/NASDAQCOM) | NASDAQ Composite | 1971 |
| `fred_VIXCLS.csv` | [FRED](https://fred.stlouisfed.org/series/VIXCLS) | VIX | 1990 |
| `fred_DGS10.csv` | [FRED](https://fred.stlouisfed.org/series/DGS10) | Rendite 10-jährige US-Staatsanleihen, % | 1962 |
| `fred_DFF.csv` | [FRED](https://fred.stlouisfed.org/series/DFF) | Federal Funds Rate, % | 1954 |
| `fred_DTWEXBGS.csv` | [FRED](https://fred.stlouisfed.org/series/DTWEXBGS) | handelsgewichteter US-Dollar-Index (Broad) | 2006 |
| `yahoo_gold_futures.csv` | Yahoo Finance (`GC=F`) | Gold-Future COMEX, USD je Feinunze (OHLC) | 2000-08-30 |
| `yahoo_sp500.csv` | Yahoo Finance (`^GSPC`) | S&P 500, volle Historie (OHLC) | 1970 |
| `farside_btc_etf_flows.csv` | [Farside Investors](https://farside.co.uk/bitcoin-etf-flow-all-data/) | tägliche Netto-Zuflüsse je US-Spot-ETF, Mio. USD | 2024-01-11 |

## Hinweise

- **Realized Cap und Transaktionsvolumen:** `CapRealUSD` und `TxTfrValAdjUSD` sind in der Coin
  Metrics Community API nicht frei verfügbar. Realized Cap wird als `CapMrktCurUSD / CapMVRVCur`
  berechnet (`nvm.metrics.realized_cap`). Das Volumen für NVT kommt von blockchain.com und ist eine
  Schätzung. Bessere Alternative: Coin Metrics Pro (Uni-Zugang?) oder eine eigene Dune-Abfrage.
- **Farside:** Tabelle wie veröffentlicht. Abflüsse stehen in Klammern, z. B. `(95.1)`, und `-` heißt
  kein Wert; beim Einlesen umwandeln. Die Website ist keine offizielle API und kann sich ändern.
- **Yahoo Finance:** inoffizielle Schnittstelle ohne Gewähr. Für das Paper als Quelle angeben
  und bei Gold ggf. mit LBMA-Preisen (World Gold Council, Registrierung nötig) gegenprüfen.
- **Handelstage:** FRED und Yahoo haben nur Börsentage, Bitcoin-Daten alle 7 Wochentage.
  Beim Zusammenführen in `02_build_panel.py` entscheiden, wie Wochenenden behandelt werden.
- **Nicht erreichbar:** SoSoValue (blockt automatische Abrufe), Stooq (verlangt JavaScript).
