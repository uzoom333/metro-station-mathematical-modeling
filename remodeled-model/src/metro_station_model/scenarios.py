"""Scenario discovery and execution."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import load_config
from .plotting import plot_baseline, plot_scenario_comparison
from .results import save_result
from .solver import SimulationResult, simulate


def run_scenario(config_path: str | Path, output_dir: str | Path) -> SimulationResult:
    """Run and persist one scenario."""
    result = simulate(load_config(config_path))
    save_result(result, output_dir)
    return result


def run_all_scenarios(
    config_dir: str | Path, output_dir: str | Path
) -> tuple[dict[str, SimulationResult], pd.DataFrame]:
    """Run every YAML scenario and create calculated comparison artifacts."""
    config_root = Path(config_dir)
    output_root = Path(output_dir)
    results: dict[str, SimulationResult] = {}
    summaries: list[dict] = []
    for path in sorted(config_root.glob("*.yaml")):
        result = run_scenario(path, output_root / path.stem)
        results[result.config.name] = result
        from .metrics import summary_metrics

        summaries.append(summary_metrics(result))
    summary_frame = pd.DataFrame(summaries)
    summary_frame.to_csv(output_root / "scenario_summary.csv", index=False)
    baseline = results["baseline"]
    plot_baseline(baseline.frame, output_root.parent / "baseline")
    plot_scenario_comparison(
        {name: result.frame for name, result in results.items()},
        summary_frame,
        output_root,
    )
    return results, summary_frame
