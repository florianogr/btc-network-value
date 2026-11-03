"""Person C: Stock-to-Flow-Modell (Regression log(MarketCap) auf log(SF), Stabilität um Halvings).

Ausgaben: output/figures/s2f.pdf, output/tables/s2f_regression.tex, ...
"""

import matplotlib.pyplot as plt

from nvm import data, metrics, plotting


def main() -> None:
    panel = data.load_panel("monthly")

    fig, ax = plt.subplots()
    ax.plot(panel.index, metrics.log(panel["sf"]), label="log(SF)")
    plotting.mark_events(ax, etf=False)
    ax.legend()
    plotting.save_figure(fig, "s2f")
    # TODO (C): Regression, Strukturbruchtests (Halvings, ETF-Start), Tabelle


if __name__ == "__main__":
    main()
