"""Run the illustrative controller-design grid."""

from pathlib import Path

from metro_station_model.config import load_config
from metro_station_model.optimization import run_optimization, save_optimization

ROOT = Path(__file__).resolve().parents[1]
frame = run_optimization(load_config(ROOT / "configs/baseline.yaml"))
best = save_optimization(frame, ROOT / "results/optimization")
print(f"Evaluated {len(frame)} combinations and saved {len(best)} best records.")
