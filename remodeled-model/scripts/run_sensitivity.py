"""Run deterministic OAT and Latin-hypercube analyses."""

import argparse
from pathlib import Path

from metro_station_model.config import load_config
from metro_station_model.sensitivity import (
    run_latin_hypercube,
    run_oat,
    save_sensitivity,
)

parser = argparse.ArgumentParser()
parser.add_argument("--samples", type=int, default=500)
args = parser.parse_args()
ROOT = Path(__file__).resolve().parents[1]
config = load_config(ROOT / "configs/baseline.yaml")
save_sensitivity(
    run_oat(config),
    run_latin_hypercube(config, args.samples),
    ROOT / "results/sensitivity",
)
print(f"Sensitivity results regenerated with {args.samples} LHS samples.")
