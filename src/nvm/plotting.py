"""Einheitlicher Abbildungsstil: Vektor-PDF in Graustufen, Tabellen als LaTeX."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

from nvm import config

GRAYS = ["#000000", "#555555", "#999999", "#cccccc"]
LINESTYLES = ["-", "--", ":", "-."]


def set_style() -> None:
    mpl.rcParams.update(
        {
            "figure.figsize": (6.0, 3.5),
            "font.family": "serif",
            "font.size": 10,
            "axes.prop_cycle": mpl.cycler(color=GRAYS) + mpl.cycler(linestyle=LINESTYLES),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#e0e0e0",
            "grid.linewidth": 0.5,
            "lines.linewidth": 1.0,
            "legend.frameon": False,
            "savefig.bbox": "tight",
            "pdf.fonttype": 42,
        }
    )


def mark_events(ax, halvings: bool = True, etf: bool = True) -> None:
    """Zeichnet Halvings und ETF-Start als senkrechte Linien ein."""
    if halvings:
        for d in config.HALVINGS:
            ax.axvline(d, color="#777777", linewidth=0.6, linestyle=":")
    if etf:
        ax.axvline(config.ETF_START, color="#000000", linewidth=0.6, linestyle="--")


def save_figure(fig, name: str) -> None:
    """Speichert nach output/figures/<name>.pdf. Dateiname bleibt stabil für Overleaf."""
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(config.FIGURES_DIR / f"{name}.pdf")
    plt.close(fig)


def save_table(df: pd.DataFrame, name: str, float_format: str = "%.3f", **kwargs) -> None:
    """Speichert nach output/tables/<name>.tex."""
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)
    df.to_latex(config.TABLES_DIR / f"{name}.tex", float_format=float_format, **kwargs)


set_style()
