"""Run and save all configured scenarios."""

from pathlib import Path

from metro_station_model.scenarios import run_all_scenarios

ROOT = Path(__file__).resolve().parents[1]
results, _ = run_all_scenarios(ROOT / "configs", ROOT / "results/scenarios")
print(f"Completed {len(results)} scenarios.")
