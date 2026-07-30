"""Coupled-state and conservation tests."""

from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import trapezoid

from metro_station_model.config import ModelConfig, load_config
from metro_station_model.model import evaluate, initial_state
from metro_station_model.solver import simulate
from metro_station_model.validation import initial_pressure_error_pa

BASE = load_config(Path(__file__).parents[1] / "configs/baseline.yaml")


def test_initial_pressure_is_consistent() -> None:
    assert initial_pressure_error_pa(BASE.data) == pytest.approx(0, abs=1e-9)


def test_state_vector_has_required_order_and_size() -> None:
    state = initial_state(BASE.data)
    assert state.shape == (5,)
    assert np.all(state > 0)


def test_evaluation_contains_five_coupled_derivatives() -> None:
    evaluation = evaluate(0, initial_state(BASE.data), BASE.data)
    assert evaluation.derivative.shape == (5,)
    assert np.isfinite(evaluation.derivative).all()


def test_mass_change_matches_integrated_net_flow() -> None:
    data = deepcopy(BASE.data)
    # Disable the nonlinear leakage term to isolate the smooth mass-balance
    # benchmark from rapid sign changes near zero pressure difference.
    data["ventilation"]["leakage_coefficient_m3_s_sqrt_Pa"] = 0
    data["simulation"]["end_time_s"] = 300
    data["simulation"]["output_step_s"] = 1
    result = simulate(ModelConfig(data, BASE.source))
    frame = result.frame
    integrated = trapezoid(
        frame["total_mass_inflow_kg_s"] - frame["total_mass_outflow_kg_s"],
        frame["time_s"],
    )
    actual = frame["air_mass_kg"].iloc[-1] - frame["air_mass_kg"].iloc[0]
    assert actual == pytest.approx(integrated, abs=0.02)
