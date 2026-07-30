"""Mechanical ventilation control."""

from __future__ import annotations


def available_maximum(time_s: float, ventilation: dict, failure: dict) -> float:
    """Return time-dependent maximum mechanical airflow."""
    start = failure.get("start_time_s")
    failed_max = failure.get("maximum_airflow_m3_s")
    if start is not None and failed_max is not None and time_s >= start:
        return max(0.0, float(failed_max))
    return float(ventilation["maximum_airflow_m3_s"])


def ventilation_target(
    time_s: float,
    temperature_k: float,
    co2_ppm: float,
    ventilation: dict,
    failure: dict,
) -> float:
    """Calculate a nonnegative, clipped ventilation target."""
    maximum = available_maximum(time_s, ventilation, failure)
    minimum = min(float(ventilation["minimum_airflow_m3_s"]), maximum)
    if ventilation["mode"] == "fixed":
        return min(max(float(ventilation["fixed_airflow_m3_s"]), minimum), maximum)
    setpoint_k = float(ventilation["temperature_setpoint_C"]) + 273.15
    raw = (
        float(ventilation["base_airflow_m3_s"])
        + float(ventilation["temperature_gain_m3_s_per_K"])
        * max(temperature_k - setpoint_k, 0.0)
        + float(ventilation["co2_gain_m3_s_per_ppm"])
        * max(co2_ppm - float(ventilation["co2_setpoint_ppm"]), 0.0)
    )
    return min(max(raw, minimum, 0.0), maximum)
