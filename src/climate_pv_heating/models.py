import numpy as np
import pandas as pd
from .config import ModelConfig

def pv_electricity_kwh(ghi_w_m2, config: ModelConfig):
    """Hourly PV electricity screening estimate in kWh."""
    config.validate()
    ghi = np.asarray(ghi_w_m2, dtype=float)
    if np.any(ghi < 0):
        raise ValueError("Solar radiation cannot be negative")
    return ghi * config.pv_area_m2 * config.pv_efficiency * config.timestep_hours / 1000.0

def heating_degree_k(temperature_c, config: ModelConfig):
    """Temperature deficit below the heating base temperature [K]."""
    temp = np.asarray(temperature_c, dtype=float)
    return np.maximum(config.heating_base_temp_c - temp, 0.0)

def useful_heating_energy_kwh_th(temperature_c, config: ModelConfig):
    """
    Illustrative useful space-heating energy [kWh_th].

    Q = HLC * max(Tbase - Tout, 0) * dt

    This is a lumped steady-state proxy. It excludes thermal mass, internal gains,
    solar gains, ventilation dynamics, DHW, controls and calibration.
    """
    config.validate()
    delta_t = heating_degree_k(temperature_c, config)
    return (
        config.heat_loss_coefficient_w_per_k
        * delta_t
        * config.timestep_hours
        / 1000.0
    )

def heating_electricity_kwh(temperature_c, config: ModelConfig):
    """Electricity required by an illustrative constant-COP heat pump [kWh_el]."""
    useful = useful_heating_energy_kwh_th(temperature_c, config)
    return useful / config.heat_pump_cop

def evaluate_timeseries(weather: pd.DataFrame, config: ModelConfig) -> pd.DataFrame:
    required = {"time", "temperature_2m_c", "shortwave_radiation_w_m2"}
    missing = required - set(weather.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    out = weather.copy()
    out["pv_kwh_el"] = pv_electricity_kwh(out["shortwave_radiation_w_m2"], config)
    out["heating_kwh_th"] = useful_heating_energy_kwh_th(out["temperature_2m_c"], config)
    out["heating_kwh_el"] = out["heating_kwh_th"] / config.heat_pump_cop
    out["balance_kwh_el"] = out["pv_kwh_el"] - out["heating_kwh_el"]
    out["deficit_kwh_el"] = np.maximum(-out["balance_kwh_el"], 0.0)
    out["surplus_kwh_el"] = np.maximum(out["balance_kwh_el"], 0.0)
    out["direct_overlap_kwh_el"] = np.minimum(out["pv_kwh_el"], out["heating_kwh_el"])
    return out
