"""Baut aus den Rohdaten panel_daily.parquet und panel_monthly.parquet."""

import pandas as pd

from nvm import config, data, metrics


def main() -> None:
    raw = data.load_raw("coinmetrics_btc_daily").apply(pd.to_numeric, errors="coerce")
    # Metadaten-Spalten des API-Clients, in der Community-Version immer leer
    raw = raw.drop(columns=["SplyCur-status", "SplyCur-status-time"])
    tx_volume = data.load_raw("blockchain_com_estimated-transaction-volume-usd").iloc[:, 0]

    panel = raw.join(tx_volume.rename("TxVolUSD"), how="left")
    panel = panel.loc[config.SAMPLE_START : config.SAMPLE_END]
    panel["CapRealUSD"] = metrics.realized_cap(panel["CapMrktCurUSD"], panel["CapMVRVCur"])
    panel["nvt"] = metrics.nvt(panel["CapMrktCurUSD"], panel["TxVolUSD"])
    panel["sf"] = metrics.stock_to_flow(panel["SplyCur"])
    panel["metcalfe"] = metrics.metcalfe_value(panel["AdrActCnt"])

    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(config.PANEL_DAILY)
    # Monatswerte: letzter Tag des Monats (Bestandsgrößen)
    panel.resample("ME").last().to_parquet(config.PANEL_MONTHLY)
    print(f"Panel: {panel.shape[0]} Tage, {panel.shape[1]} Spalten")


if __name__ == "__main__":
    main()
