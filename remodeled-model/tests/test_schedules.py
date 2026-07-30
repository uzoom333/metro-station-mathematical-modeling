"""Schedule interpolation and event tests."""

import pytest

from metro_station_model.schedules import (
    passenger_count,
    piston_airflow,
    train_heat,
    train_present,
)


def test_piecewise_linear_occupancy() -> None:
    schedule = [[0, 4], [10, 14]]
    assert passenger_count(5, schedule, 4) == pytest.approx(9)
    assert passenger_count(-1, schedule, 4) == 4


def test_train_direct_and_residual_heat() -> None:
    assert train_heat(105, [100], 10, 1000, 500, 20) == 1000
    assert train_heat(110, [100], 10, 1000, 500, 20) == pytest.approx(500)
    assert train_present(105, [100], 10)
    assert not train_present(110, [100], 10)


def test_piston_window_surrounds_arrival_and_departure() -> None:
    assert piston_airflow(90, [100], 20, 30, 5) == 5
    assert piston_airflow(120, [100], 20, 30, 5) == 5
    assert piston_airflow(200, [100], 20, 30, 5) == 0
