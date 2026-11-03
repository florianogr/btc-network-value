"""Person B: langfristige Beziehung zwischen Preis und Netzwerkwert (ADF/KPSS, Johansen, VECM).

Ausgaben: output/tables/unit_roots.tex, output/tables/johansen.tex, ...
"""

from nvm import data, econometrics, metrics, plotting


def main() -> None:
    panel = data.load_panel("monthly")
    logs = panel[["CapMrktCurUSD", "metcalfe"]].apply(metrics.log).dropna()

    plotting.save_table(econometrics.unit_root_table(logs), "unit_roots")
    plotting.save_table(econometrics.johansen(logs), "johansen")
    # TODO (B): VECM schätzen, Anpassungskoeffizienten tabellieren, Abbildungen


if __name__ == "__main__":
    main()
