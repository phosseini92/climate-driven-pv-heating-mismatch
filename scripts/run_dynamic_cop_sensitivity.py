from pathlib import Path
import argparse
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from climate_pv_heating.io import read_epw
from climate_pv_heating.config import ModelConfig
from climate_pv_heating.models import evaluate_timeseries
from climate_pv_heating.heat_pump import dynamic_heating_electricity_kwh
from climate_pv_heating.metrics import symmetric_mismatch_index

parser = argparse.ArgumentParser()
parser.add_argument("--epw", required=True)
parser.add_argument("--output", default="outputs/tabriz_itmy/dynamic_cop_sensitivity.csv")
args = parser.parse_args()

weather, _ = read_epw(args.epw)
cfg = ModelConfig()
base = evaluate_timeseries(weather, cfg)

rows = []
scenarios = [
    {"label": "constant_cop_3", "mode": "constant"},
    {"label": "linear_mild", "mode": "linear", "slope_per_k": 0.04},
    {"label": "linear_baseline", "mode": "linear", "slope_per_k": 0.06},
    {"label": "linear_steeper", "mode": "linear", "slope_per_k": 0.08},
]

for s in scenarios:
    if s["mode"] == "constant":
        h_el = base["heating_kwh_th"].to_numpy() / 3.0
        mean_cop = 3.0
    else:
        h_el, cop = dynamic_heating_electricity_kwh(
            base["heating_kwh_th"].to_numpy(),
            base["temperature_2m_c"].to_numpy(),
            slope_per_k=s["slope_per_k"],
        )
        mean_cop = float(cop[base["heating_kwh_th"].to_numpy() > 0].mean())

    pv = base["pv_kwh_el"].to_numpy()
    overlap = float(pd.Series([min(a, b) for a, b in zip(pv, h_el)]).sum())
    total_h = float(h_el.sum())

    rows.append({
        "scenario": s["label"],
        "annual_heating_kwh_el": total_h,
        "mean_cop_during_heating": mean_cop,
        "direct_pv_coverage_ratio": overlap / total_h if total_h > 0 else 0.0,
        "symmetric_mismatch_index": symmetric_mismatch_index(pv, h_el),
    })

out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out, index=False, float_format="%.8f")
print(pd.DataFrame(rows).to_string(index=False))
