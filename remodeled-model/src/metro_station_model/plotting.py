"""Reusable, non-interactive plots generated from calculated outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def plot_baseline(frame: pd.DataFrame, directory: str | Path) -> list[Path]:
    """Generate the eight baseline diagnostic figures."""
    target = Path(directory)
    created: list[Path] = []

    specifications = [
        (
            "temperature.png",
            [("air_temperature_C", "Air"), ("structure_temperature_C", "Structure")],
            "Air and effective structural temperature",
            "Temperature (°C)",
        ),
        ("co2.png", [("co2_ppm", "CO₂")], "CO₂ concentration", "CO₂ (ppm)"),
        (
            "pressure.png",
            [("pressure_difference_Pa", "Inside − outside")],
            "Internal pressure difference",
            "Pressure difference (Pa)",
        ),
        (
            "ventilation.png",
            [
                ("ventilation_airflow_m3_s", "Actual"),
                ("target_ventilation_airflow_m3_s", "Target"),
            ],
            "Mechanical ventilation",
            "Airflow (m³/s)",
        ),
        (
            "heat_sources.png",
            [
                ("passenger_heat_W", "Passengers"),
                ("train_heat_W", "Train"),
                ("equipment_heat_W", "Equipment"),
            ],
            "Heat contributions",
            "Heat rate (W)",
        ),
        (
            "air_changes.png",
            [("air_changes_per_hour", "Mechanical ventilation")],
            "Mechanical air changes per hour",
            "Air changes per hour (1/h)",
        ),
    ]
    for filename, lines, title, ylabel in specifications:
        fig, axis = plt.subplots(figsize=(8, 4.5))
        for column, label in lines:
            axis.plot(frame["time_min"], frame[column], label=label)
        axis.set(xlabel="Time (min)", ylabel=ylabel, title=title)
        axis.set_xlim(frame["time_min"].min(), frame["time_min"].max())
        axis.grid(alpha=0.25)
        if len(lines) > 1:
            axis.legend()
        path = target / filename
        _save(fig, path)
        created.append(path)

    fig, left = plt.subplots(figsize=(8, 4.5))
    left.plot(frame["time_min"], frame["passengers"], color="tab:blue")
    left.set(xlabel="Time (min)", ylabel="Passengers", title="Occupancy and trains")
    right = left.twinx()
    right.fill_between(
        frame["time_min"],
        0,
        frame["train_present"].astype(float),
        alpha=0.25,
        color="tab:red",
        label="Train present",
    )
    right.set_ylabel("Train present (0/1)")
    path = target / "occupancy_trains.png"
    _save(fig, path)
    created.append(path)

    fig, left = plt.subplots(figsize=(8, 4.5))
    left.plot(frame["time_min"], frame["fan_power_proxy_W"] / 1000, label="Power")
    left.set(xlabel="Time (min)", ylabel="Fan power proxy (kW)")
    right = left.twinx()
    right.plot(
        frame["time_min"],
        frame["cumulative_fan_energy_kWh"],
        color="tab:orange",
        label="Energy",
    )
    right.set_ylabel("Cumulative fan-energy proxy (kWh)")
    left.set_title("Illustrative fan-energy proxy")
    path = target / "fan_energy.png"
    _save(fig, path)
    created.append(path)
    return created


def plot_scenario_comparison(
    frames: dict[str, pd.DataFrame], summaries: pd.DataFrame, directory: str | Path
) -> list[Path]:
    """Generate comparison lines and metric bars for all scenarios."""
    target = Path(directory)
    created: list[Path] = []
    lines = [
        ("air_temperature_C", "scenario_temperature.png", "Air temperature", "°C"),
        ("co2_ppm", "scenario_co2.png", "CO₂ concentration", "ppm"),
        (
            "ventilation_airflow_m3_s",
            "scenario_ventilation.png",
            "Mechanical ventilation",
            "m³/s",
        ),
    ]
    for column, filename, title, unit in lines:
        fig, axis = plt.subplots(figsize=(9, 5))
        for name, frame in frames.items():
            axis.plot(frame["time_min"], frame[column], label=name)
        axis.set(
            xlabel="Time (min)", ylabel=unit, title=f"Scenario comparison: {title}"
        )
        axis.grid(alpha=0.2)
        axis.legend(fontsize=7, ncol=2)
        path = target / filename
        _save(fig, path)
        created.append(path)
    bars = [
        (
            "maximum_air_temperature_C",
            "maximum_temperature.png",
            "Maximum air temperature",
            "°C",
        ),
        ("maximum_co2_ppm", "maximum_co2.png", "Maximum CO₂", "ppm"),
        (
            "total_fan_energy_proxy_kWh",
            "fan_energy_comparison.png",
            "Fan-energy proxy",
            "kWh",
        ),
        (
            "maximum_absolute_pressure_difference_Pa",
            "maximum_pressure_difference.png",
            "Maximum absolute pressure difference",
            "Pa",
        ),
    ]
    for column, filename, title, unit in bars:
        fig, axis = plt.subplots(figsize=(9, 5))
        axis.bar(summaries["scenario"], summaries[column])
        axis.set(ylabel=unit, title=title)
        axis.tick_params(axis="x", rotation=35)
        path = target / filename
        _save(fig, path)
        created.append(path)
    return created
