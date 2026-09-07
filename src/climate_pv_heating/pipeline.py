from pathlib import Path
import json
import hashlib
import pandas as pd
from .config import ModelConfig
from .models import evaluate_timeseries
from .metrics import summarize_timeseries, monthly_summary
from .plots import (
    plot_temperature_and_radiation,
    plot_energy_timeseries,
    plot_monthly_balance,
)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def run_pipeline(weather: pd.DataFrame, output_dir, config=None, make_plots=True):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    config = config or ModelConfig()

    ts = evaluate_timeseries(weather, config)
    summary = summarize_timeseries(ts)
    monthly = monthly_summary(ts)

    ts_path = output_dir / "timeseries.csv"
    summary_path = output_dir / "summary.json"
    monthly_path = output_dir / "monthly_summary.csv"
    config_path = output_dir / "model_config.json"

    ts.to_csv(ts_path, index=False, float_format="%.8f")
    monthly.to_csv(monthly_path, index=False, float_format="%.8f")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    config_path.write_text(json.dumps(config.__dict__, indent=2, sort_keys=True), encoding="utf-8")

    if make_plots:
        plot_temperature_and_radiation(ts, output_dir / "weather_inputs.png")
        plot_energy_timeseries(ts, output_dir / "pv_vs_heating.png")
        plot_monthly_balance(monthly, output_dir / "monthly_balance.png")

    tracked = [ts_path, summary_path, monthly_path, config_path]
    manifest = {p.name: sha256(p) for p in tracked}
    (output_dir / "manifest_sha256.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    return ts, summary, monthly, manifest
