import numpy as np
import pandas as pd

def symmetric_mismatch_index(pv, heating):
    """
    Energy-weighted temporal mismatch index in [0, 1].

    0 -> perfect match at every timestep
    1 -> no temporal overlap (or only one series has energy)
    """
    pv = np.asarray(pv, dtype=float)
    heating = np.asarray(heating, dtype=float)
    denom = np.sum(pv + heating)
    if denom <= 0:
        return 0.0
    return float(np.sum(np.abs(pv - heating)) / denom)

def summarize_timeseries(df: pd.DataFrame) -> dict:
    pv = float(df["pv_kwh_el"].sum())
    hth = float(df["heating_kwh_th"].sum())
    hel = float(df["heating_kwh_el"].sum())
    overlap = float(df["direct_overlap_kwh_el"].sum())
    deficit = float(df["deficit_kwh_el"].sum())
    surplus = float(df["surplus_kwh_el"].sum())

    return {
        "annual_pv_kwh_el": pv,
        "annual_heating_kwh_th": hth,
        "annual_heating_kwh_el": hel,
        "direct_overlap_kwh_el": overlap,
        "direct_pv_coverage_ratio": overlap / hel if hel > 0 else 0.0,
        "annual_deficit_kwh_el": deficit,
        "annual_surplus_kwh_el": surplus,
        "deficit_hour_fraction": float((df["balance_kwh_el"] < 0).mean()),
        "surplus_hour_fraction": float((df["balance_kwh_el"] > 0).mean()),
        "symmetric_mismatch_index": symmetric_mismatch_index(
            df["pv_kwh_el"], df["heating_kwh_el"]
        ),
    }

def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()
    tmp["time"] = pd.to_datetime(tmp["time"])
    tmp["month"] = tmp["time"].dt.to_period("M").astype(str)
    grouped = tmp.groupby("month", as_index=False).agg(
        pv_kwh_el=("pv_kwh_el", "sum"),
        heating_kwh_el=("heating_kwh_el", "sum"),
        deficit_kwh_el=("deficit_kwh_el", "sum"),
        surplus_kwh_el=("surplus_kwh_el", "sum"),
        direct_overlap_kwh_el=("direct_overlap_kwh_el", "sum"),
        mean_temperature_c=("temperature_2m_c", "mean"),
    )
    grouped["net_balance_kwh_el"] = grouped["pv_kwh_el"] - grouped["heating_kwh_el"]
    return grouped
