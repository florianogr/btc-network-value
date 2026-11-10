"""Zeigt die beiden Panels (täglich und monatlich) als Tabelle im Browser an. Nur zum Anschauen.

    uv run python scripts/Daten_Test.py

Schreibt data/local/panels.html (nicht in Git) und öffnet die Datei im Browser.
Die Spaltennamen und das Datum bleiben beim Scrollen stehen.
Vorher muss das Panel gebaut sein: uv run python scripts/02_build_panel.py
"""

import webbrowser

import pandas as pd

from nvm import config, data

TARGET = config.DATA_DIR / "local" / "panels.html"

CSS = """
body { font: 13px -apple-system, system-ui, sans-serif; margin: 0; background: #fff; color: #111; }
nav { position: sticky; top: 0; z-index: 3; background: #222; padding: 8px 16px; }
nav a { color: #fff; margin-right: 16px; text-decoration: none; font-weight: 600; }
h2 { margin: 24px 16px 4px; }
p { margin: 0 16px 8px; color: #555; }
.wrap { max-height: 80vh; overflow: auto; margin: 0 16px; border: 1px solid #ccc; }
table { border-collapse: collapse; font-variant-numeric: tabular-nums; }
th, td { padding: 3px 8px; border-bottom: 1px solid #eee; white-space: nowrap; text-align: right; }
thead th { position: sticky; top: 0; z-index: 2; background: #f2f2f2;
           border-bottom: 2px solid #999; }
tbody th { position: sticky; left: 0; z-index: 1; background: #fafafa; text-align: left; }
thead th:first-child { left: 0; z-index: 3; }
tbody tr:hover td, tbody tr:hover th { background: #fff6d5; }
"""


def section(name: str, df: pd.DataFrame) -> str:
    df = df.copy()
    df.index = df.index.strftime("%Y-%m-%d")
    df.index.name = "Datum"
    table = df.to_html(float_format="{:,.4f}".format, na_rep="", border=0)
    missing = ", ".join(f"{c}: {n}" for c, n in df.isna().sum().items() if n) or "keine"
    return (
        f'<h2 id="{name}">{name}</h2>'
        f"<p>{df.shape[0]} Zeilen × {df.shape[1]} Spalten, {df.index[0]} bis {df.index[-1]}. "
        f"Fehlende Werte: {missing}</p>"
        f'<div class="wrap">{table}</div>'
    )


def main() -> None:
    panels = {"panel_daily": data.load_panel("daily"), "panel_monthly": data.load_panel("monthly")}
    nav = "".join(f'<a href="#{name}">{name}</a>' for name in panels)
    body = "".join(section(name, df) for name, df in panels.items())
    html = (
        f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Panels</title>'
        f"<style>{CSS}</style></head><body><nav>{nav}</nav>{body}</body></html>"
    )
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(html, encoding="utf-8")
    print(f"geschrieben: {TARGET}")
    webbrowser.open(TARGET.as_uri())


if __name__ == "__main__":
    main()
