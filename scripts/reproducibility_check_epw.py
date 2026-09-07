from pathlib import Path
import argparse
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from climate_pv_heating.io import read_epw
from climate_pv_heating.pipeline import run_pipeline
from climate_pv_heating.config import ModelConfig

parser = argparse.ArgumentParser()
parser.add_argument("--epw", required=True)
args = parser.parse_args()

a = ROOT / "outputs/_repro_epw_a"
b = ROOT / "outputs/_repro_epw_b"
for p in (a, b):
    if p.exists():
        shutil.rmtree(p)

weather, _ = read_epw(args.epw)
cfg = ModelConfig()

_, _, _, ma = run_pipeline(weather, a, cfg, make_plots=False)
_, _, _, mb = run_pipeline(weather, b, cfg, make_plots=False)

if ma != mb:
    raise SystemExit("FAIL: tracked EPW-driven CSV/JSON outputs differ across repeated runs")

print("PASS: Tabriz EPW-driven tracked CSV/JSON outputs are byte-identical across repeated runs")
