"""Deterministic integration and tabular post-processing."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.integrate import cumulative_trapezoid, solve_ivp

from .config import ModelConfig
from .conversions import kelvin_to_celsius
from .model import evaluate, initial_state
from .physics import fan_power_proxy


@dataclass(frozen=True)
class SimulationResult:
    """Calculated time series plus solver diagnostics."""

    frame: pd.DataFrame
    solver_success: bool
    solver_message: str
    function_evaluations: int
    config: ModelConfig


def _time_grid(start: float, end: float, step: float) -> np.ndarray:
    count = int(np.floor((end - start) / step))
    grid = start + np.arange(count + 1) * step
    if grid[-1] < end:
        grid = np.append(grid, end)
    return grid


def simulate(config: ModelConfig) -> SimulationResult:
    """Integrate the configured model and return deterministic outputs."""
    cfg = config.data
    settings = cfg["simulation"]
    times = _time_grid(
        settings["start_time_s"], settings["end_time_s"], settings["output_step_s"]
    )
    solution = solve_ivp(
        lambda time, state: evaluate(time, state, cfg).derivative,
        (settings["start_time_s"], settings["end_time_s"]),
        initial_state(cfg),
        method=settings["method"],
        t_eval=times,
        rtol=settings["relative_tolerance"],
        atol=settings["absolute_tolerance"],
    )
    if not solution.success:
        raise RuntimeError(f"Solver failed: {solution.message}")
    rows = []
    for index, time_s in enumerate(solution.t):
        state = solution.y[:, index]
        evaluation = evaluate(float(time_s), state, cfg)
        row = {
            "time_s": time_s,
            "time_min": time_s / 60.0,
            **evaluation.diagnostics,
            "ventilation_airflow_m3_s": state[4],
            "air_mass_kg": state[0],
            "structure_temperature_K": state[2],
            "structure_temperature_C": kelvin_to_celsius(state[2]),
            "outdoor_temperature_C": cfg["outdoor"]["temperature_C"],
            "outdoor_pressure_Pa": cfg["outdoor"]["pressure_Pa"],
            "co2_moles": state[3],
        }
        row["air_temperature_C"] = kelvin_to_celsius(row["air_temperature_K"])
        row["air_changes_per_hour"] = (
            row["ventilation_airflow_m3_s"] * 3600.0 / cfg["station"]["volume_m3"]
        )
        row["fan_power_proxy_W"] = fan_power_proxy(
            row["ventilation_airflow_m3_s"],
            cfg["fan"]["reference_power_W"],
            cfg["fan"]["reference_airflow_m3_s"],
        )
        rows.append(row)
    frame = pd.DataFrame(rows)
    frame["cumulative_fan_energy_kWh"] = (
        cumulative_trapezoid(frame["fan_power_proxy_W"], frame["time_s"], initial=0.0)
        / 3.6e6
    )
    if not np.isfinite(frame.select_dtypes(include=[np.number])).all().all():
        raise RuntimeError("Simulation produced NaN or infinite values")
    if (frame["air_mass_kg"] <= 0).any() or (frame["air_temperature_K"] <= 0).any():
        raise RuntimeError("Simulation produced a nonphysical state")
    return SimulationResult(
        frame, solution.success, solution.message, solution.nfev, config
    )
