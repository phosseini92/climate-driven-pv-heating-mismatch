from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from climate_pv_heating.synthetic import generate_synthetic_hourly_year
from climate_pv_heating.sensitivity import run_sensitivity_grid
from climate_pv_heating.plots import plot_sensitivity

weather = generate_synthetic_hourly_year(2023)
result = run_sensitivity_grid(weather)
out = ROOT / "outputs/sensitivity"
out.mkdir(parents=True, exist_ok=True)
result.to_csv(out / "sensitivity_grid.csv", index=False, float_format="%.8f")
plot_sensitivity(result, out / "sensitivity_hlc.png")
print(f"Sensitivity complete: {len(result)} scenarios")
