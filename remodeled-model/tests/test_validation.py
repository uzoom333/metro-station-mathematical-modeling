"""Analytical numerical-method benchmarks."""

import numpy as np
from scipy.integrate import solve_ivp

from metro_station_model.validation import (
    analytical_first_order_temperature,
    analytical_mixed_concentration,
)


def test_analytical_co2_benchmark() -> None:
    """Constant-volume mixing follows its first-order analytical solution."""
    times = np.linspace(0, 600, 121)
    initial, outdoor, rate = 600.0, 420.0, 0.01
    numerical = solve_ivp(
        lambda _time, value: rate * (outdoor - value),
        (times[0], times[-1]),
        [initial],
        t_eval=times,
        rtol=1e-10,
        atol=1e-11,
    ).y[0]
    analytical = analytical_mixed_concentration(times, initial, outdoor, rate)
    assert np.max(np.abs(numerical - analytical)) < 1e-5


def test_analytical_thermal_benchmark() -> None:
    """Constant-coefficient thermal response follows exponential decay."""
    times = np.linspace(0, 1000, 101)
    initial, equilibrium, rate = 310.0, 300.0, 0.002
    numerical = solve_ivp(
        lambda _time, value: rate * (equilibrium - value),
        (times[0], times[-1]),
        [initial],
        t_eval=times,
        rtol=1e-10,
        atol=1e-11,
    ).y[0]
    analytical = analytical_first_order_temperature(times, initial, equilibrium, rate)
    assert np.max(np.abs(numerical - analytical)) < 1e-7
