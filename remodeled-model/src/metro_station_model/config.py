"""Configuration loading, inheritance, and validation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


@dataclass(frozen=True)
class ModelConfig:
    """Validated, fully resolved model configuration."""

    data: dict[str, Any]
    source: Path

    def section(self, name: str) -> dict[str, Any]:
        """Return a named configuration section."""
        return self.data[name]

    @property
    def name(self) -> str:
        """Return the scenario name."""
        return str(self.data["metadata"]["name"])


def validate_config(data: dict[str, Any]) -> None:
    """Reject inconsistent or nonphysical configuration values."""
    required = {
        "metadata",
        "station",
        "thermal",
        "air_quality",
        "outdoor",
        "initial_conditions",
        "ventilation",
        "occupancy",
        "train",
        "fan",
        "failure",
        "simulation",
    }
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Missing configuration sections: {sorted(missing)}")
    metadata = data["metadata"]
    if (
        metadata["data_status"] != "synthetic_illustrative"
        or metadata["engineering_validation"] is not False
        or metadata["original_submission_data"] is not False
    ):
        raise ValueError("Required academic-honesty metadata is invalid")
    station = data["station"]
    volume = station["length_m"] * station["width_m"] * station["average_height_m"]
    if station["volume_m3"] <= 0 or abs(volume - station["volume_m3"]) > 1.0e-6:
        raise ValueError("Station dimensions must multiply to volume_m3")
    thermal = data["thermal"]
    positive_thermal = [
        "air_structure_conductance_W_per_K",
        "structure_outdoor_UA_W_per_K",
        "structure_thermal_capacitance_J_per_K",
    ]
    if any(thermal[key] <= 0 for key in positive_thermal):
        raise ValueError("Thermal capacitances and conductances must be positive")
    vent = data["ventilation"]
    if vent["mode"] not in {"demand_controlled", "fixed"}:
        raise ValueError("Ventilation mode must be demand_controlled or fixed")
    if not 0 <= vent["minimum_airflow_m3_s"] <= vent["maximum_airflow_m3_s"]:
        raise ValueError("Ventilation airflow limits are not ordered")
    if vent["base_airflow_m3_s"] > vent["maximum_airflow_m3_s"]:
        raise ValueError("Base airflow exceeds maximum airflow")
    if vent["actuator_time_constant_s"] <= 0:
        raise ValueError("Actuator time constant must be positive")
    schedule = data["occupancy"]["schedule"]
    times = [float(point[0]) for point in schedule]
    values = [float(point[1]) for point in schedule]
    if len(schedule) < 2 or times != sorted(times) or len(set(times)) != len(times):
        raise ValueError("Occupancy schedule times must be strictly increasing")
    if min(values) < data["occupancy"]["minimum_passengers"]:
        raise ValueError("Occupancy falls below the configured minimum")
    train = data["train"]
    if train["dwell_time_s"] < 0 or train["piston_event_duration_s"] < 0:
        raise ValueError("Train durations cannot be negative")
    simulation = data["simulation"]
    if (
        simulation["end_time_s"] <= simulation["start_time_s"]
        or simulation["output_step_s"] <= 0
    ):
        raise ValueError("Simulation time settings are invalid")


def load_config(path: str | Path) -> ModelConfig:
    """Load a YAML file and recursively resolve its optional baseline."""
    source = Path(path).resolve()
    with source.open(encoding="utf-8") as stream:
        raw = yaml.safe_load(stream)
    parent = raw.pop("extends", None)
    if parent:
        base = load_config(source.parent / parent).data
        raw = _merge(base, raw)
    validate_config(raw)
    return ModelConfig(raw, source)
