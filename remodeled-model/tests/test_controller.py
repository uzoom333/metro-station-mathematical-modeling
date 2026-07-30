"""Demand-controlled ventilation tests."""

from pathlib import Path

from metro_station_model.config import load_config
from metro_station_model.controller import ventilation_target

CONFIG = load_config(Path(__file__).parents[1] / "configs/baseline.yaml").data
VENT = CONFIG["ventilation"]
FAILURE = CONFIG["failure"]
SETPOINT_K = VENT["temperature_setpoint_C"] + 273.15


def target(temperature_k: float, co2_ppm: float) -> float:
    return ventilation_target(0, temperature_k, co2_ppm, VENT, FAILURE)


def test_minimum_clipping() -> None:
    modified = dict(VENT, base_airflow_m3_s=0)
    assert ventilation_target(0, SETPOINT_K, 420, modified, FAILURE) == 10


def test_maximum_clipping() -> None:
    assert target(SETPOINT_K + 100, 10000) == 100


def test_no_demand() -> None:
    assert target(SETPOINT_K, 420) == 25


def test_temperature_demand() -> None:
    assert target(SETPOINT_K + 1, 420) == 31


def test_co2_demand() -> None:
    assert target(SETPOINT_K, 1100) == 30


def test_combined_demand() -> None:
    assert target(SETPOINT_K + 1, 1100) == 36


def test_fixed_mode() -> None:
    fixed = dict(VENT, mode="fixed")
    assert ventilation_target(0, SETPOINT_K + 20, 5000, fixed, FAILURE) == 35


def test_failure_reduces_available_maximum() -> None:
    failure = {"start_time_s": 10, "maximum_airflow_m3_s": 20}
    assert ventilation_target(10, SETPOINT_K + 20, 5000, VENT, failure) == 20


def test_target_is_never_negative() -> None:
    modified = dict(VENT, minimum_airflow_m3_s=0, base_airflow_m3_s=-5)
    assert ventilation_target(0, SETPOINT_K, 420, modified, FAILURE) == 0
