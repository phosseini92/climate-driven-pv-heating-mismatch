from pathlib import Path
import pandas as pd

EPW_COLUMNS = [
    "year", "month", "day", "hour", "minute", "data_source_flags",
    "dry_bulb_c", "dew_point_c", "relative_humidity_pct", "station_pressure_pa",
    "extraterrestrial_horizontal_wh_m2", "extraterrestrial_direct_normal_wh_m2",
    "horizontal_infrared_wh_m2", "global_horizontal_radiation_wh_m2",
    "direct_normal_radiation_wh_m2", "diffuse_horizontal_radiation_wh_m2",
    "global_horizontal_illuminance_lux", "direct_normal_illuminance_lux",
    "diffuse_horizontal_illuminance_lux", "zenith_luminance_cd_m2",
    "wind_direction_deg", "wind_speed_m_s", "total_sky_cover_tenths",
    "opaque_sky_cover_tenths", "visibility_km", "ceiling_height_m",
    "present_weather_observation", "present_weather_codes",
    "precipitable_water_mm", "aerosol_optical_depth_thousandths",
    "snow_depth_cm", "days_since_last_snowfall",
    "albedo", "liquid_precipitation_depth_mm",
    "liquid_precipitation_quantity_hr"
]

def read_open_meteo_csv(path):
    """Read a clean weather CSV produced by a compatible fetch pipeline."""
    df = pd.read_csv(path)
    required = {"time", "temperature_2m_c", "shortwave_radiation_w_m2"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Observed CSV missing columns: {sorted(missing)}")
    df["time"] = pd.to_datetime(df["time"])
    return df

def read_epw(path):
    """
    Parse an EnergyPlus EPW weather file into the three columns required by the model.

    EPW hour values run from 1 to 24 and refer to the end of the hourly interval.
    The workflow maps them to interval-start timestamps by subtracting one hour.

    Global horizontal radiation in EPW is Wh/m² for the preceding hour.
    For an hourly timestep, its numeric value is equivalent to an hourly-average W/m².
    """
    path = Path(path)
    with path.open("r", encoding="utf-8", errors="replace") as f:
        header = [next(f).rstrip("\n") for _ in range(8)]

    df = pd.read_csv(
        path,
        skiprows=8,
        header=None,
        names=EPW_COLUMNS,
        usecols=range(len(EPW_COLUMNS)),
    )

    required = ["year", "month", "day", "hour", "dry_bulb_c", "global_horizontal_radiation_wh_m2"]
    if df[required].isna().any().any():
        raise ValueError("EPW contains missing values in required fields")

    # Many typical-year EPWs use arbitrary source years. Month/day/hour order is the primary calendar.
    base_year = 2001  # non-leap reference year for consistent comparison
    time = pd.to_datetime(
        {
            "year": base_year,
            "month": df["month"].astype(int),
            "day": df["day"].astype(int),
            "hour": 0,
        }
    ) + pd.to_timedelta(df["hour"].astype(int) - 1, unit="h")

    out = pd.DataFrame(
        {
            "time": time,
            "temperature_2m_c": df["dry_bulb_c"].astype(float),
            "shortwave_radiation_w_m2": df["global_horizontal_radiation_wh_m2"].astype(float),
            "source": "energyplus_epw",
        }
    )
    return out, header
