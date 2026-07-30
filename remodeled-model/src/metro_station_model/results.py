"""Portable result persistence."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import yaml

from . import __version__
from .metrics import summary_metrics
from .solver import SimulationResult


def save_result(result: SimulationResult, directory: str | Path) -> dict:
    """Save CSV, JSON summary, resolved YAML, and generation metadata."""
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    result.frame.to_csv(target / "time_series.csv", index=False)
    metrics = summary_metrics(result)
    (target / "summary.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8"
    )
    (target / "config_resolved.yaml").write_text(
        yaml.safe_dump(result.config.data, sort_keys=False), encoding="utf-8"
    )
    settings = result.config.data["simulation"]
    metadata = {
        "model_version": __version__,
        "scenario": result.config.name,
        "data_status": "synthetic_illustrative",
        "engineering_validation": False,
        "original_submission_data": False,
        "random_seed": settings["random_seed"],
        "solver": settings["method"],
        "relative_tolerance": settings["relative_tolerance"],
        "absolute_tolerance": settings["absolute_tolerance"],
        "solver_function_evaluations": result.function_evaluations,
        "solver_success": result.solver_success,
        "generation_timestamp_utc": datetime.now(UTC).isoformat(),
    }
    (target / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8"
    )
    return metrics
