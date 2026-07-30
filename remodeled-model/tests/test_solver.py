"""Solver invariants, equilibrium, and scenario smoke tests."""

from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest

from metro_station_model.config import ModelConfig, load_config
from metro_station_model.solver import simulate

CONFIGS = Path(__file__).parents[1] / "configs"
BASE = load_config(CONFIGS / "baseline.yaml")


def shortened(config: ModelConfig, duration: float = 60) -> ModelConfig:
    data = deepcopy(config.data)
    data["simulation"]["end_time_s"] = duration
    data["simulation"]["output_step_s"] = 10
    return ModelConfig(data, config.source)


def test_solver_outputs_are_physical_and_ordered() -> None:
    result = simulate(shortened(BASE))
    numeric = result.frame.select_dtypes(include=[np.number])
    assert result.solver_success
    assert np.isfinite(numeric).all().all()
    assert (result.frame["air_mass_kg"] > 0).all()
    assert (result.frame["air_temperature_K"] > 0).all()
    assert result.frame["time_s"].is_monotonic_increasing


def test_no_source_equilibrium_remains_constant() -> None:
    data = deepcopy(BASE.data)
    outdoor_c = data["outdoor"]["temperature_C"]
    outdoor_co2 = data["air_quality"]["outdoor_co2_ppm"]
    data["occupancy"]["minimum_passengers"] = 0
    data["occupancy"]["schedule"] = [[0, 0], [300, 0]]
    data["train"]["arrival_times_s"] = []
    data["thermal"]["equipment_heat_W"] = 0
    data["initial_conditions"]["air_temperature_C"] = outdoor_c
    data["initial_conditions"]["structure_temperature_C"] = outdoor_c
    data["initial_conditions"]["co2_ppm"] = outdoor_co2
    data["ventilation"]["mode"] = "fixed"
    data["initial_conditions"]["ventilation_airflow_m3_s"] = 25
    data["ventilation"]["fixed_airflow_m3_s"] = 25
    data["simulation"]["end_time_s"] = 300
    data["simulation"]["output_step_s"] = 10
    result = simulate(ModelConfig(data, BASE.source))
    assert result.frame["air_temperature_C"].to_numpy() == pytest.approx(outdoor_c)
    assert result.frame["co2_ppm"].to_numpy() == pytest.approx(outdoor_co2)
    assert result.frame["air_mass_kg"].max() - result.frame["air_mass_kg"].min() < 1e-8


@pytest.mark.parametrize("path", sorted(CONFIGS.glob("*.yaml")), ids=lambda p: p.stem)
def test_scenario_smoke(path: Path) -> None:
    result = simulate(shortened(load_config(path)))
    assert result.solver_success
