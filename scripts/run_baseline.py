from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from climate_pv_heating.synthetic import generate_synthetic_hourly_year
from climate_pv_heating.pipeline import run_pipeline
from climate_pv_heating.config import ModelConfig

weather = generate_synthetic_hourly_year(2023)
weather.to_csv(ROOT / "data/synthetic/synthetic_hourly_2023.csv", index=False, float_format="%.6f")

config = ModelConfig(
    pv_area_m2=30.0,
    pv_efficiency=0.18,
    heating_base_temp_c=18.0,
    heat_loss_coefficient_w_per_k=120.0,
    heat_pump_cop=3.0,
)

_, summary, _, _ = run_pipeline(weather, ROOT / "outputs/baseline", config=config)
print("Baseline complete")
for k, v in summary.items():
    print(f"{k}: {v:.6f}")
