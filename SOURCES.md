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

## Stichprobe und Vorlauf

- **Analysezeitraum:** 01.01.2012 – 30.06.2026 (`config.SAMPLE_START`, `config.SAMPLE_END`), also
  5.295 Tage bzw. 174 Monate. Die Out-of-sample-Phase beginnt am 01.01.2020.
- **Vorlauf aus 2011:** Die Rohdaten reichen weiter zurück (Coin Metrics bis 2009, blockchain.com bis
  August 2010). Daten vor 2012 fließen nicht in die Analyse ein. Sie werden nur als Vorlauf für
  gleitende Kennzahlen genutzt, damit diese am 01.01.2012 schon einen Wert haben:
  - NVT Signal: die letzten 90 Tage von 2011
  - NVT über 365 Tage (Robustheit) und Stock-to-Flow: das ganze Jahr 2011
- **Panel:** `scripts/02_build_panel.py` berechnet die Kennzahlen auf der ganzen Historie und
  schneidet erst danach auf den Analysezeitraum zu. Im Analysezeitraum fehlt bei keiner Kennzahl
  ein Wert. Das Skript bricht ab, falls doch.

## Kennzahlen

| Spalte | Formel | Umsetzung |
|---|---|---|
| `CapRealUSD` | `CapMrktCurUSD / CapMVRVCur` | `metrics.realized_cap` |
| `nvt` | `CapMrktCurUSD` / Mittel von `TxVolUSD` über 90 Tage, mind. 80 Tage vorhanden | `metrics.nvt` (NVT Signal nach Kalichkin 2018) |
| `nvt_365` | wie `nvt`, über 365 Tage, mind. 330 Tage vorhanden | Robustheit, analog zum Jahresgewinn im KGV |
| `sf` | `SplyCur / (SplyCur − SplyCur vor 365 Tagen)` | `metrics.stock_to_flow` |
| `metcalfe` | `AdrActCnt²` (Skalierung wird in der Regression geschätzt) | `metrics.metcalfe_value` |

Fenstergrößen und Mindestzahl der Tage stehen in `src/nvm/config.py`.

## Hinweise

- **Realized Cap und Transaktionsvolumen:** `CapRealUSD` und `TxTfrValAdjUSD` sind in der Coin
  Metrics Community API nicht frei verfügbar. Realized Cap wird deshalb als
  `CapMrktCurUSD / CapMVRVCur` berechnet (`nvm.metrics.realized_cap`). Das Volumen für NVT kommt
  von blockchain.com und ist eine Schätzung. Bessere Alternativen wären Coin Metrics Pro
  (Uni-Zugang?) oder eine eigene Dune-Abfrage.
- **Lücken bei blockchain.com:** Zwischen 28.08.2010 und 28.10.2026 fehlen rund 20 Tage. Im
  Analysezeitraum sind es 8 einzelne Tage: 11.12.2021, 21.12.2021, 24.12.2021, 14.07.2023,
  14.11.2023, 30.06.2024, 18.11.2024 und 24.06.2025. Die Rohdaten werden nicht aufgefüllt.
  `TxVolUSD` ist an diesen Tagen im Panel leer. Das NVT mittelt über die vorhandenen Tage. Im
  ungünstigsten 90-Tage-Fenster sind 87 Tage vorhanden (Dezember 2021), im ungünstigsten
  365-Tage-Fenster 351.

## Abgerufen, aber nicht verwendet

Diese Daten waren im ersten Datenstand enthalten. Am 10.11.2026 wurden sie entfernt, weil die
Aufgabe keine Kontrollvariablen verlangt. Sie bleiben in der Git-Historie (Commit `414a4dc`).

- **FRED:** SP500, NASDAQCOM, VIXCLS, DGS10, DFF, DTWEXBGS
- **Yahoo Finance:** Gold-Future (`GC=F`) und S&P 500 (`^GSPC`)
- **Farside Investors:** tägliche Zuflüsse in US-Spot-Bitcoin-ETFs

## Getestet, aber nicht erreichbar

- **SoSoValue** (<https://sosovalue.com/>): blockt automatische Abrufe
- **Stooq** (<https://stooq.com/>): der Download verlangt JavaScript
