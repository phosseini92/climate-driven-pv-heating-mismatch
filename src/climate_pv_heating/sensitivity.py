from itertools import product
import pandas as pd
from .config import ModelConfig
from .models import evaluate_timeseries
from .metrics import summarize_timeseries

def run_sensitivity_grid(
    weather: pd.DataFrame,
    heating_base_temps=(18.0, 20.0),
    hlc_values=(80.0, 120.0, 160.0),
    cop_values=(2.5, 3.0, 4.0),
    pv_areas=(20.0, 30.0, 40.0),
    pv_efficiency=0.18,
):
    rows = []
    for tbase, hlc, cop, area in product(
        heating_base_temps, hlc_values, cop_values, pv_areas
    ):
        cfg = ModelConfig(
            pv_area_m2=area,
            pv_efficiency=pv_efficiency,
            heating_base_temp_c=tbase,
            heat_loss_coefficient_w_per_k=hlc,
            heat_pump_cop=cop,
        )
        ts = evaluate_timeseries(weather, cfg)
        s = summarize_timeseries(ts)
        rows.append({
            "heating_base_temp_c": tbase,
            "hlc_w_per_k": hlc,
            "heat_pump_cop": cop,
            "pv_area_m2": area,
            **s,
        })
    return pd.DataFrame(rows)
