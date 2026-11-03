# btc-network-value

Seminararbeit: Netzwerkwert-Modelle für Bitcoin (NVT, Metcalfe, Stock-to-Flow, Kointegration/VECM).

## Einrichten (einmalig)

Voraussetzung: [uv](https://docs.astral.sh/uv/getting-started/installation/) und Git.

```bash
git clone https://github.com/florianogr/btc-network-value.git
cd btc-network-value
uv sync                          # identische Umgebung aus uv.lock
uv run nbstripout --install      # Notebook-Ausgaben vor jedem Commit löschen
cp .env.example .env             # API-Keys eintragen, .env nie committen
```

## Alles reproduzieren

```bash
uv run python scripts/run_all.py
```

Erzeugt aus dem eingefrorenen Datenstand in `data/raw/2026-11-03/` das Panel in
`data/processed/` sowie alle Abbildungen (`output/figures/*.pdf`) und Tabellen
(`output/tables/*.tex`). `scripts/01_download.py` läuft nur einmal beim Einfrieren
des Datenstands und ist nicht Teil von `run_all.py`.

## Struktur

```
data/raw/<datum>/        eingefrorener Datenstand, nie bearbeiten (Herkunft in SOURCES.md)
data/processed/          panel_daily.parquet, panel_monthly.parquet (wird erzeugt)
src/nvm/config.py        Zeiträume, Halving-Daten, ETF-Start, Snapshot-Datum
src/nvm/data.py          Download + Laden
src/nvm/metrics.py       Realized Cap, NVT, SF, Metcalfe
src/nvm/econometrics.py  ADF/KPSS, Kointegration, VECM, Granger, OOS-R²
src/nvm/plotting.py      einheitlicher Abbildungsstil (Graustufen-PDF, LaTeX-Tabellen)
scripts/                 01_download, 02_build_panel, 03_long_run (B), 04_prediction (A), 05_s2f (C), run_all
notebooks/               nur zum Ausprobieren, Dateiname mit Initialen beginnen (z. B. fo_nvt.ipynb)
output/                  figures/ und tables/ für Overleaf
```

## Regeln

- **Ein Datenstand.** Analysen lesen nur aus `data/processed/` über `nvm.data.load_panel()`.
- **Konstanten nur in `src/nvm/config.py`.** Stichprobe, OOS-Start, Halvings, ETF-Start.
- **Notebooks zum Ausprobieren, Skripte für Ergebnisse.** Was in die Arbeit kommt, erzeugt `run_all.py`.
- **Branches und Pull Requests.** Eigener Branch je Person (`a/nvt`, `b/vecm`, `c/s2f`),
  Merge in `main` nur per Pull Request nach Review durch eine andere Person.
- **Output im Paper-Format.** Abbildungen über `plotting.save_figure()`, Tabellen über
  `plotting.save_table()`. Keine Zahlen von Hand abtippen.
- **Geheimnisse in `.env`.** Wird über `python-dotenv` geladen.

## Arbeitsablauf

```bash
git switch main && git pull
git switch -c a/nvt              # bzw. b/vecm, c/s2f
# ... arbeiten ...
uv run ruff check . && uv run python scripts/run_all.py
git add -A && git commit -m "NVT: Granger-Tests"
git push -u origin a/nvt         # dann Pull Request auf GitHub öffnen
```

Neues Paket: `uv add <paket>`, dann `pyproject.toml` und `uv.lock` mitcommitten.

## Overleaf

Dateien aus `output/figures/` und `output/tables/` hochladen, sobald Ergebnisse feststehen.
Die Dateinamen bleiben stabil, bei Änderungen also nur ersetzen.

```latex
\includegraphics{figures/nvt.pdf}
\input{tables/johansen.tex}
```

## Termine

| Meilenstein | Datum |
|---|---|
| Ergebnisse festhalten | 06.12.2026 |
| Rohfassung | 20.12.2026 |
| Abgabe | 20.01.2027 |
