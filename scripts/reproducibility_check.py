from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from climate_pv_heating.synthetic import generate_synthetic_hourly_year
from climate_pv_heating.pipeline import run_pipeline
from climate_pv_heating.config import ModelConfig

a = ROOT / "outputs/_repro_a"
b = ROOT / "outputs/_repro_b"
for p in (a, b):
    if p.exists():
        shutil.rmtree(p)

weather = generate_synthetic_hourly_year(2023)
cfg = ModelConfig()

_, _, _, ma = run_pipeline(weather, a, cfg, make_plots=False)
_, _, _, mb = run_pipeline(weather, b, cfg, make_plots=False)

if ma != mb:
    raise SystemExit("FAIL: tracked data outputs differ across repeated runs")

print("PASS: tracked CSV/JSON outputs are byte-identical across repeated runs")
