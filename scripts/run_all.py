"""Erzeugt alle Abbildungen und Tabellen der Arbeit aus dem eingefrorenen Datenstand.

    uv run python scripts/run_all.py

Was in der Arbeit steht, muss dieses Skript erzeugen.
"""

import runpy
from pathlib import Path

STEPS = ["02_build_panel.py", "03_long_run.py", "04_prediction.py", "05_s2f.py"]


def main() -> None:
    here = Path(__file__).parent
    for step in STEPS:
        print(f"== {step}")
        runpy.run_path(str(here / step), run_name="__main__")


if __name__ == "__main__":
    main()
