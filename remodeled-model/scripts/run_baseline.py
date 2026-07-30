"""Run and save the baseline simulation."""

from pathlib import Path

from metro_station_model.config import load_config
from metro_station_model.plotting import plot_baseline
from metro_station_model.results import save_result
from metro_station_model.solver import simulate

ROOT = Path(__file__).resolve().parents[1]
result = simulate(load_config(ROOT / "configs/baseline.yaml"))
save_result(result, ROOT / "results/baseline")
plot_baseline(result.frame, ROOT / "results/baseline")
print("Baseline results regenerated.")
