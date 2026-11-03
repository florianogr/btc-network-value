"""Person A: Prognosekraft des NVT (Granger, Out-of-sample-R² ab OOS_START).

Ausgaben: output/figures/nvt.pdf, output/tables/granger_nvt.tex, ...
"""

import matplotlib.pyplot as plt

from nvm import config, data, plotting


def main() -> None:
    panel = data.load_panel("daily")

    fig, ax = plt.subplots()
    ax.plot(panel.index, panel["nvt"], label="NVT-Signal (90 Tage)")
    ax.axvline(config.OOS_START, color="black", linewidth=0.8)
    plotting.mark_events(ax)
    ax.set_yscale("log")
    ax.legend()
    plotting.save_figure(fig, "nvt")
    # TODO (A): Renditen bilden, Granger-Tests, rollierende Prognosen, oos_r2


if __name__ == "__main__":
    main()
