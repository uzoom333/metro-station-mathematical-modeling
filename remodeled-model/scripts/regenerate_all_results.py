"""Safely regenerate every committed Version 2 result artifact."""

from pathlib import Path

from metro_station_model.config import load_config
from metro_station_model.optimization import run_optimization, save_optimization
from metro_station_model.scenarios import run_all_scenarios
from metro_station_model.sensitivity import (
    run_latin_hypercube,
    run_oat,
    save_sensitivity,
)

ROOT = Path(__file__).resolve().parents[1]
RESULTS = (ROOT / "results").resolve()


def clear_generated_results() -> None:
    """Delete generated files only inside known result subdirectories."""
    allowed = [
        RESULTS / name
        for name in ("baseline", "scenarios", "sensitivity", "optimization")
    ]
    for directory in allowed:
        directory.mkdir(parents=True, exist_ok=True)
        if RESULTS not in directory.resolve().parents:
            raise RuntimeError(f"Refusing unsafe result path: {directory}")
        for path in sorted(directory.rglob("*"), reverse=True):
            if path.is_file() and path.name != "README.md":
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()


def main() -> None:
    """Regenerate scenarios, sensitivity, optimization, tables, and plots."""
    clear_generated_results()
    config = load_config(ROOT / "configs/baseline.yaml")
    scenarios, summary = run_all_scenarios(ROOT / "configs", RESULTS / "scenarios")
    save_sensitivity(
        run_oat(config), run_latin_hypercube(config, 500), RESULTS / "sensitivity"
    )
    combinations = run_optimization(config)
    best = save_optimization(combinations, RESULTS / "optimization")
    if not all(result.solver_success for result in scenarios.values()):
        raise RuntimeError("At least one scenario solver failed")
    print(
        f"Generated {len(scenarios)} scenarios, {len(summary)} summaries, "
        f"500 LHS samples, {len(combinations)} optimization runs, "
        f"and {len(best)} selected configurations."
    )


if __name__ == "__main__":
    main()
