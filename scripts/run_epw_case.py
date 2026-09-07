from pathlib import Path
import argparse
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from climate_pv_heating.io import read_epw
from climate_pv_heating.pipeline import run_pipeline
from climate_pv_heating.config import ModelConfig

parser = argparse.ArgumentParser()
parser.add_argument("--epw", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

weather, header = read_epw(args.epw)
config = ModelConfig()
_, summary, _, _ = run_pipeline(weather, args.output, config=config)

out = Path(args.output)
(out / "epw_header.txt").write_text("\n".join(header) + "\n", encoding="utf-8")

print(f"Parsed {len(weather)} EPW hourly records")
for k, v in summary.items():
    print(f"{k}: {v:.6f}")
