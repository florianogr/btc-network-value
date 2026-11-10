"""Baut aus den Rohdaten panel_daily.parquet und panel_monthly.parquet."""

import pandas as pd

from nvm import config, data, metrics


def main() -> None:
    raw = data.load_raw("coinmetrics_btc_daily").apply(pd.to_numeric, errors="coerce")
    # Metadaten-Spalten des API-Clients, in der Community-Version immer leer
    raw = raw.drop(columns=["SplyCur-status", "SplyCur-status-time"])
    tx_volume = data.load_raw("blockchain_com_estimated-transaction-volume-usd").iloc[:, 0]

    # Lückenloser Tagesindex: fehlende Tage werden zu NaN-Zeilen, damit gleitende Fenster
    # Kalendertage zählen.
    days = pd.date_range(raw.index.min(), raw.index.max(), freq="D", name="time")
    panel = raw.reindex(days).join(tx_volume.rename("TxVolUSD"), how="left")

    # Kennzahlen auf der ganzen Historie berechnen, erst danach auf die Stichprobe zuschneiden.
    # So liefern die Tage vor SAMPLE_START den Vorlauf (NVT: 90 bzw. 365 Tage, S2F: 365 Tage).
    panel["CapRealUSD"] = metrics.realized_cap(panel["CapMrktCurUSD"], panel["CapMVRVCur"])
    panel["nvt"] = metrics.nvt(
        panel["CapMrktCurUSD"], panel["TxVolUSD"], config.NVT_WINDOW, config.NVT_MIN_DAYS
    )
    panel["nvt_365"] = metrics.nvt(
        panel["CapMrktCurUSD"],
        panel["TxVolUSD"],
        config.NVT_WINDOW_ROBUST,
        config.NVT_MIN_DAYS_ROBUST,
    )
    panel["sf"] = metrics.stock_to_flow(panel["SplyCur"])
    panel["metcalfe"] = metrics.metcalfe_value(panel["AdrActCnt"])

    panel = panel.loc[config.SAMPLE_START : config.SAMPLE_END]
    missing = panel.drop(columns="TxVolUSD").isna().sum()
    if missing.any():
        raise SystemExit(f"Fehlende Werte in der Stichprobe:\n{missing[missing > 0]}")

    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(config.PANEL_DAILY)
    # Monatswerte: letzter Tag des Monats (Bestandsgrößen)
    panel.resample("ME").last().to_parquet(config.PANEL_MONTHLY)
    print(f"Panel: {panel.shape[0]} Tage, {panel.shape[1]} Spalten")


if __name__ == "__main__":
    main()
