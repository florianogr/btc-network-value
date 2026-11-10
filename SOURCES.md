# Datenquellen

Jede Datei in `data/raw/` steht hier mit Quelle, Abrufzeitpunkt und dem Skript, das sie erzeugt hat.
Rohdaten werden nach dem Download nie bearbeitet.

| | |
|---|---|
| Datenstand | `data/raw/2026-11-03/` |
| Abgerufen | 03.11.2026, 22:23 Uhr MEZ (UTC+1), von Florian |
| Skript | `scripts/01_download.py` (Funktionen in `src/nvm/data.py`) |
| Software | Python 3.12, Versionen aller Pakete in `uv.lock` |

## Übersicht

| Datei | Quelle | Abgerufen | Zeitraum | Zeilen |
|---|---|---|---|---|
| `coinmetrics_btc_daily.csv` | Coin Metrics Community API | 03.11.2026, 22:23:38 MEZ | 03.01.2009 – 02.11.2026 | 6.513 |
| `blockchain_com_estimated-transaction-volume-usd.csv` | blockchain.com Charts API | 03.11.2026, 22:23:38 MEZ | 28.08.2010 – 28.10.2026 | 5.884 |

Die Uhrzeiten sind die Zeitstempel der gespeicherten Dateien.

## [1] Coin Metrics – Community Network Data

- **Anbieter:** Coin Metrics Inc.
- **Website:** <https://coinmetrics.io/community-network-data/>
- **Dokumentation:** <https://docs.coinmetrics.io/api/v4/>
- **Endpunkt:** `https://community-api.coinmetrics.io/v4/timeseries/asset-metrics`, abgerufen über
  das Python-Paket `coinmetrics-api-client` mit Asset `btc`, Frequenz `1d` und Start 03.01.2009
  (`config.DOWNLOAD_START`). Ohne API-Key, also die freie Community-Version.
- **Lizenz:** Creative Commons BY-NC 4.0. Coin Metrics muss als Quelle genannt werden.
- **Datei:** `coinmetrics_btc_daily.csv`

| Metrik | Inhalt | Verwendet für | Daten ab |
|---|---|---|---|
| `PriceUSD` | Preis in USD | alle Modelle | 18.07.2010 |
| `CapMrktCurUSD` | Marktkapitalisierung in USD | NVT, Metcalfe, S2F, MVRV | 18.07.2010 |
| `CapMVRVCur` | MVRV-Verhältnis | Realized Cap = `CapMrktCurUSD / CapMVRVCur` | 18.07.2010 |
| `AdrActCnt` | aktive Adressen pro Tag | Metcalfe | 03.01.2009 |
| `SplyCur` | umlaufende Menge in BTC | Stock-to-Flow (Bestand) | 03.01.2009 |
| `IssTotNtv` | neu geschürfte BTC pro Tag | Stock-to-Flow (Zufluss) | 09.01.2009 |
| `TxCnt` | Anzahl Transaktionen pro Tag | Robustheit, Manipulierbarkeit | 03.01.2009 |
| `HashRate` | Hashrate | derzeit nicht verwendet | 09.01.2009 |

Alle Metriken enden am 02.11.2026. Die mitgelieferten Spalten `SplyCur-status` und
`SplyCur-status-time` sind leer. `02_build_panel.py` übernimmt sie nicht ins Panel.

**Zitiervorschlag:** Coin Metrics (2026): Community Network Data, Bitcoin, Tagesdaten.
<https://coinmetrics.io/community-network-data/>, abgerufen am 03.11.2026.

## [2] blockchain.com – Charts API

- **Anbieter:** Blockchain.com
- **Website:** <https://www.blockchain.com/explorer/charts/estimated-transaction-volume-usd>
- **Endpunkt:**
  `https://api.blockchain.info/charts/estimated-transaction-volume-usd?timespan=all&format=json&sampled=false`
- **Inhalt:** geschätztes On-chain-Transaktionsvolumen in USD pro Tag. Verwendet für NVT und Velocity.
- **Nutzung:** frei abrufbar, es gelten die Nutzungsbedingungen von Blockchain.com.
- **Datei:** `blockchain_com_estimated-transaction-volume-usd.csv`

**Zitiervorschlag:** Blockchain.com (2026): Estimated Transaction Value (USD).
<https://www.blockchain.com/explorer/charts/estimated-transaction-volume-usd>, abgerufen am 03.11.2026.

## Ereignisdaten (in `src/nvm/config.py`)

- **Bitcoin-Halvings** bei den Blockhöhen 210.000, 420.000, 630.000 und 840.000: 28.11.2012,
  09.07.2016, 11.05.2020 und 20.04.2024. Nachprüfbar über einen Block-Explorer, z. B.
  <https://www.blockchain.com/explorer>.
- **Start der US-Spot-Bitcoin-ETFs:** 11.01.2024. Das ist der erste Handelstag nach der Genehmigung
  durch die SEC am 10.01.2024 (<https://www.sec.gov/>). Das Datum dient nur als Bruchdatum, die
  ETF-Flüsse selbst werden nicht verwendet.

## Hinweise

- **Realized Cap und Transaktionsvolumen:** `CapRealUSD` und `TxTfrValAdjUSD` sind in der Coin
  Metrics Community API nicht frei verfügbar. Realized Cap wird deshalb als
  `CapMrktCurUSD / CapMVRVCur` berechnet (`nvm.metrics.realized_cap`). Das Volumen für NVT kommt
  von blockchain.com und ist eine Schätzung. Bessere Alternativen wären Coin Metrics Pro
  (Uni-Zugang?) oder eine eigene Dune-Abfrage.
- **Lücken bei blockchain.com:** Zwischen 28.08.2010 und 28.10.2026 fehlen rund 20 Tage. Die
  Reihe endet einige Tage vor dem Ende der Stichprobe (31.10.2026).

## Abgerufen, aber nicht verwendet

Diese Daten waren im ersten Datenstand enthalten. Am 10.11.2026 wurden sie entfernt, weil die
Aufgabe keine Kontrollvariablen verlangt. Sie bleiben in der Git-Historie (Commit `414a4dc`).

- **FRED:** SP500, NASDAQCOM, VIXCLS, DGS10, DFF, DTWEXBGS
- **Yahoo Finance:** Gold-Future (`GC=F`) und S&P 500 (`^GSPC`)
- **Farside Investors:** tägliche Zuflüsse in US-Spot-Bitcoin-ETFs

## Getestet, aber nicht erreichbar

- **SoSoValue** (<https://sosovalue.com/>): blockt automatische Abrufe
- **Stooq** (<https://stooq.com/>): der Download verlangt JavaScript
