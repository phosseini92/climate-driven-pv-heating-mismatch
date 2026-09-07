import numpy as np
import pandas as pd

def generate_synthetic_hourly_year(year: int = 2023) -> pd.DataFrame:
    """
    Deterministic cold-temperate synthetic benchmark.

    The benchmark is intentionally transparent rather than meteorologically predictive:
    - hourly resolution;
    - seasonal + diurnal air-temperature cycles;
    - seasonally varying daylight duration and solar peak;
    - no random noise.
    """
    start = pd.Timestamp(f"{year}-01-01 00:00:00")
    end = pd.Timestamp(f"{year+1}-01-01 00:00:00")
    time = pd.date_range(start, end, freq="h", inclusive="left")

    df = pd.DataFrame({"time": time})
    doy = df["time"].dt.dayofyear.to_numpy()
    hour = df["time"].dt.hour.to_numpy() + 0.5

    # Seasonal mean: approx. -2 C mid-winter to 20 C mid-summer.
    seasonal_temp = 9.0 + 11.0 * np.cos(2 * np.pi * (doy - 200) / 365.0)
    # Diurnal range: approx. +/- 3 C, warmest mid-afternoon.
    diurnal_temp = 3.0 * np.cos(2 * np.pi * (hour - 15.0) / 24.0)
    temperature_c = seasonal_temp + diurnal_temp

    # Simplified day length: ~8 h winter, ~16 h summer.
    day_length = 12.0 + 4.0 * np.cos(2 * np.pi * (doy - 172) / 365.0)
    sunrise = 12.0 - day_length / 2.0
    solar_phase = (hour - sunrise) / day_length
    daylight = (solar_phase > 0.0) & (solar_phase < 1.0)

    # Peak GHI: ~250 W/m2 winter to ~800 W/m2 summer.
    peak_ghi = 250.0 + 550.0 * (day_length - 8.0) / 8.0
    ghi = np.zeros(len(df), dtype=float)
    ghi[daylight] = peak_ghi[daylight] * np.sin(np.pi * solar_phase[daylight])

    df["temperature_2m_c"] = temperature_c
    df["shortwave_radiation_w_m2"] = np.clip(ghi, 0.0, None)
    df["source"] = "synthetic_cold_temperate_benchmark"
    return df
