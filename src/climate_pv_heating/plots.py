from pathlib import Path
import matplotlib.pyplot as plt

def _save(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)

def plot_temperature_and_radiation(df, path):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(df["time"], df["temperature_2m_c"], label="Temperature (°C)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_xlabel("Time")
    ax2 = ax.twinx()
    ax2.plot(df["time"], df["shortwave_radiation_w_m2"], alpha=0.55, label="Shortwave radiation")
    ax2.set_ylabel("Shortwave radiation (W/m²)")
    ax.set_title("Weather inputs")
    _save(fig, path)

def plot_energy_timeseries(df, path):
    daily = df.copy()
    daily["date"] = daily["time"].dt.date
    daily = daily.groupby("date", as_index=False).agg(
        pv_kwh_el=("pv_kwh_el", "sum"),
        heating_kwh_el=("heating_kwh_el", "sum"),
    )
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(daily["date"], daily["pv_kwh_el"], label="PV electricity")
    ax.plot(daily["date"], daily["heating_kwh_el"], label="Heating electricity")
    ax.set_ylabel("Daily energy (kWh)")
    ax.set_xlabel("Date")
    ax.set_title("Daily PV generation vs electrified heating demand")
    ax.legend()
    _save(fig, path)

def plot_monthly_balance(monthly, path):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.bar(monthly["month"], monthly["net_balance_kwh_el"])
    ax.axhline(0, linewidth=0.8)
    ax.set_ylabel("PV - heating electricity (kWh)")
    ax.set_xlabel("Month")
    ax.set_title("Monthly electricity balance")
    ax.tick_params(axis="x", rotation=45)
    _save(fig, path)

def plot_sensitivity(df, path):
    # Plot the effect of HLC for the baseline Tbase=18, COP=3, PV area=30 slice.
    sub = df[
        (df["heating_base_temp_c"] == 18.0)
        & (df["heat_pump_cop"] == 3.0)
        & (df["pv_area_m2"] == 30.0)
    ].sort_values("hlc_w_per_k")
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.plot(sub["hlc_w_per_k"], sub["symmetric_mismatch_index"], marker="o")
    ax.set_xlabel("Heat-loss coefficient (W/K)")
    ax.set_ylabel("Symmetric mismatch index")
    ax.set_title("Mismatch sensitivity to building heat loss")
    _save(fig, path)
