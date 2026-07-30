"""Calculated summary metrics and selected analysis thresholds."""

from __future__ import annotations

import numpy as np
from scipy.integrate import trapezoid

from .solver import SimulationResult


def _integral(values: np.ndarray, times: np.ndarray) -> float:
    return float(trapezoid(values, times))


def summary_metrics(result: SimulationResult) -> dict[str, float | bool | int | str]:
    """Calculate reproducible metrics from a simulation result."""
    frame = result.frame
    time = frame["time_s"].to_numpy()
    duration = time[-1] - time[0]
    metrics: dict[str, float | bool | int | str] = {
        "scenario": result.config.name,
        "maximum_air_temperature_C": float(frame["air_temperature_C"].max()),
        "mean_air_temperature_C": _integral(frame["air_temperature_C"], time)
        / duration,
        "maximum_structure_temperature_C": float(
            frame["structure_temperature_C"].max()
        ),
        "maximum_co2_ppm": float(frame["co2_ppm"].max()),
        "mean_co2_ppm": _integral(frame["co2_ppm"], time) / duration,
        "maximum_absolute_pressure_difference_Pa": float(
            frame["pressure_difference_Pa"].abs().max()
        ),
        "mean_ventilation_airflow_m3_s": _integral(
            frame["ventilation_airflow_m3_s"], time
        )
        / duration,
        "maximum_ventilation_airflow_m3_s": float(
            frame["ventilation_airflow_m3_s"].max()
        ),
        "total_fan_energy_proxy_kWh": float(
            frame["cumulative_fan_energy_kWh"].iloc[-1]
        ),
        "total_passenger_heat_kWh": _integral(frame["passenger_heat_W"], time) / 3.6e6,
        "total_train_heat_kWh": _integral(frame["train_heat_W"], time) / 3.6e6,
        "time_above_27_C_s": _integral(
            (frame["air_temperature_C"] > 27.0).astype(float), time
        ),
        "time_above_29_C_s": _integral(
            (frame["air_temperature_C"] > 29.0).astype(float), time
        ),
        "time_above_1000_ppm_s": _integral(
            (frame["co2_ppm"] > 1000.0).astype(float), time
        ),
        "time_above_1200_ppm_s": _integral(
            (frame["co2_ppm"] > 1200.0).astype(float), time
        ),
        "minimum_air_mass_kg": float(frame["air_mass_kg"].min()),
        "maximum_air_mass_kg": float(frame["air_mass_kg"].max()),
        "minimum_air_changes_per_hour": float(frame["air_changes_per_hour"].min()),
        "mean_air_changes_per_hour": _integral(frame["air_changes_per_hour"], time)
        / duration,
        "maximum_air_changes_per_hour": float(frame["air_changes_per_hour"].max()),
        "solver_function_evaluations": result.function_evaluations,
        "solver_success": result.solver_success,
        "analysis_threshold_note": (
            "27/29 °C and 1000/1200 ppm are illustrative experiment targets, "
            "not universal regulatory limits."
        ),
    }
    return metrics
