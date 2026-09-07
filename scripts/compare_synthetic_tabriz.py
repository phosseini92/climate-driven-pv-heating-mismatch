from pathlib import Path
import argparse
import json
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--synthetic", default="outputs/baseline/summary.json")
parser.add_argument("--tabriz", default="outputs/tabriz_itmy/summary.json")
parser.add_argument("--output", default="outputs/comparison")
args = parser.parse_args()

syn = json.loads(Path(args.synthetic).read_text())
tab = json.loads(Path(args.tabriz).read_text())

metrics = [
    "annual_pv_kwh_el",
    "annual_heating_kwh_th",
    "annual_heating_kwh_el",
    "direct_pv_coverage_ratio",
    "annual_deficit_kwh_el",
    "annual_surplus_kwh_el",
    "deficit_hour_fraction",
    "symmetric_mismatch_index",
]

rows = []
for m in metrics:
    rows.append({
        "metric": m,
        "synthetic_benchmark": syn[m],
        "tabriz_itmy": tab[m],
        "difference_tabriz_minus_synthetic": tab[m] - syn[m],
    })

out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
df = pd.DataFrame(rows)
df.to_csv(out / "synthetic_vs_tabriz_metrics.csv", index=False, float_format="%.8f")

# Plot only dimensionless metrics together to avoid mixing units.
plot_metrics = ["direct_pv_coverage_ratio", "deficit_hour_fraction", "symmetric_mismatch_index"]
plot_df = df[df["metric"].isin(plot_metrics)].copy()
x = range(len(plot_df))
width = 0.35

fig, ax = plt.subplots(figsize=(8.5, 4.8))
ax.bar([i - width/2 for i in x], plot_df["synthetic_benchmark"], width, label="Synthetic")
ax.bar([i + width/2 for i in x], plot_df["tabriz_itmy"], width, label="Tabriz ITMY")
ax.set_xticks(list(x))
ax.set_xticklabels(plot_df["metric"], rotation=20, ha="right")
ax.set_ylabel("Ratio / index")
ax.set_title("Synthetic benchmark vs Tabriz ITMY")
ax.legend()
fig.tight_layout()
fig.savefig(out / "synthetic_vs_tabriz_dimensionless.png", dpi=180, bbox_inches="tight")
plt.close(fig)

print(df.to_string(index=False))
