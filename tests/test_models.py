import numpy as np
import pandas as pd
from climate_pv_heating.config import ModelConfig
from climate_pv_heating.models import (
    pv_electricity_kwh,
    useful_heating_energy_kwh_th,
    heating_electricity_kwh,
    evaluate_timeseries,
)

def test_pv_zero_at_zero_radiation():
    cfg = ModelConfig()
    assert pv_electricity_kwh([0.0], cfg)[0] == 0.0

def test_pv_energy_unit_conversion():
    cfg = ModelConfig(pv_area_m2=10, pv_efficiency=0.2, timestep_hours=1)
    # 1000 W/m2 * 10 m2 * 0.2 * 1h = 2 kWh
    assert np.isclose(pv_electricity_kwh([1000], cfg)[0], 2.0)

def test_heating_zero_above_base():
    cfg = ModelConfig(heating_base_temp_c=18)
    assert useful_heating_energy_kwh_th([20], cfg)[0] == 0.0

def test_heating_proxy_unit_conversion():
    cfg = ModelConfig(
        heating_base_temp_c=18,
        heat_loss_coefficient_w_per_k=100,
        timestep_hours=1,
    )
    # 100 W/K * 10 K * 1h = 1 kWh_th
    assert np.isclose(useful_heating_energy_kwh_th([8], cfg)[0], 1.0)

def test_higher_cop_reduces_electricity():
    low = ModelConfig(heat_pump_cop=2)
    high = ModelConfig(heat_pump_cop=4)
    assert heating_electricity_kwh([0], high)[0] < heating_electricity_kwh([0], low)[0]

def test_higher_hlc_increases_heating():
    low = ModelConfig(heat_loss_coefficient_w_per_k=80)
    high = ModelConfig(heat_loss_coefficient_w_per_k=160)
    assert useful_heating_energy_kwh_th([0], high)[0] > useful_heating_energy_kwh_th([0], low)[0]

def test_higher_pv_area_increases_generation():
    low = ModelConfig(pv_area_m2=20)
    high = ModelConfig(pv_area_m2=40)
    assert pv_electricity_kwh([500], high)[0] > pv_electricity_kwh([500], low)[0]

def test_evaluate_timeseries_columns():
    df = pd.DataFrame({
        "time": pd.date_range("2023-01-01", periods=2, freq="h"),
        "temperature_2m_c": [0.0, 20.0],
        "shortwave_radiation_w_m2": [0.0, 500.0],
    })
    out = evaluate_timeseries(df, ModelConfig())
    for col in ["pv_kwh_el", "heating_kwh_th", "heating_kwh_el", "balance_kwh_el"]:
        assert col in out.columns
