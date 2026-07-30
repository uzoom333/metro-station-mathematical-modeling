"""Illustrative ventilation-control design experiment."""

from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from itertools import product
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .config import ModelConfig
from .metrics import summary_metrics
from .solver import simulate

BASE_FLOWS = [10, 15, 20, 25, 30, 35, 40, 45, 50]
MAXIMUM_FLOWS = [50, 60, 70, 80, 90, 100, 110, 120]
TEMPERATURE_GAINS = [0, 2, 4, 6, 8]
CO2_GAINS = [0, 0.02, 0.04, 0.06, 0.08]


def _calculate_metrics(payload: tuple[dict, str]) -> dict:
    data, source = payload
    return summary_metrics(simulate(ModelConfig(data, Path(source))))


def run_optimization(config: ModelConfig) -> pd.DataFrame:
    """Evaluate the full controller grid using demonstration constraints."""
    inputs = []
    for base, maximum, temperature_gain, co2_gain in product(
        BASE_FLOWS, MAXIMUM_FLOWS, TEMPERATURE_GAINS, CO2_GAINS
    ):
        if maximum < base:
            continue
        data = deepcopy(config.data)
        vent = data["ventilation"]
        vent["base_airflow_m3_s"] = float(base)
        vent["maximum_airflow_m3_s"] = float(maximum)
        vent["temperature_gain_m3_s_per_K"] = float(temperature_gain)
        vent["co2_gain_m3_s_per_ppm"] = float(co2_gain)
        inputs.append((base, maximum, temperature_gain, co2_gain, data))
    workers = min(8, os.cpu_count() or 1)
    payloads = [(data, str(config.source)) for *_, data in inputs]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        calculated = list(executor.map(_calculate_metrics, payloads, chunksize=4))
    rows = []
    for (base, maximum, temperature_gain, co2_gain, _), metrics in zip(
        inputs, calculated, strict=True
    ):
        feasible = (
            metrics["maximum_air_temperature_C"] <= 29.0
            and metrics["maximum_co2_ppm"] <= 1200.0
            and metrics["maximum_absolute_pressure_difference_Pa"] <= 100.0
        )
        rows.append(
            {
                "base_airflow_m3_s": base,
                "maximum_airflow_m3_s": maximum,
                "temperature_gain_m3_s_per_K": temperature_gain,
                "co2_gain_m3_s_per_ppm": co2_gain,
                **metrics,
                "feasible": feasible,
            }
        )
    return pd.DataFrame(rows)


def _best_solutions(feasible: pd.DataFrame) -> pd.DataFrame:
    if feasible.empty:
        return pd.DataFrame(columns=["criterion"])
    candidates = []
    criteria = {
        "minimum_energy": "total_fan_energy_proxy_kWh",
        "lowest_base_airflow": "base_airflow_m3_s",
        "lowest_maximum_airflow": "maximum_airflow_m3_s",
    }
    for label, column in criteria.items():
        row = feasible.loc[feasible[column].idxmin()].copy()
        row["criterion"] = label
        candidates.append(row)
    balance_columns = [
        "total_fan_energy_proxy_kWh",
        "maximum_air_temperature_C",
        "maximum_co2_ppm",
        "maximum_absolute_pressure_difference_Pa",
    ]
    normalized = feasible[balance_columns].apply(
        lambda column: (
            (column - column.min()) / max(float(column.max() - column.min()), 1.0e-12)
        )
    )
    row = feasible.loc[normalized.mean(axis=1).idxmin()].copy()
    row["criterion"] = "balanced_normalized_metrics"
    candidates.append(row)
    return pd.DataFrame(candidates)


def save_optimization(frame: pd.DataFrame, directory: str | Path) -> pd.DataFrame:
    """Save all, feasible, best, and trade-off artifacts."""
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    feasible = frame[frame["feasible"]].copy()
    best = _best_solutions(feasible)
    frame.to_csv(target / "all_combinations.csv", index=False)
    feasible.to_csv(target / "feasible_combinations.csv", index=False)
    best.to_csv(target / "best_configurations.csv", index=False)
    for output, filename, label in [
        (
            "maximum_air_temperature_C",
            "energy_vs_maximum_temperature.png",
            "Maximum air temperature (°C)",
        ),
        ("maximum_co2_ppm", "energy_vs_maximum_co2.png", "Maximum CO₂ (ppm)"),
    ]:
        fig, axis = plt.subplots(figsize=(7, 5))
        axis.scatter(
            frame[output],
            frame["total_fan_energy_proxy_kWh"],
            c=frame["feasible"].map({True: "tab:green", False: "tab:gray"}),
            s=12,
            alpha=0.6,
        )
        axis.set(
            xlabel=label,
            ylabel="Fan-energy proxy (kWh)",
            title="Illustrative controller design experiment",
        )
        fig.tight_layout()
        fig.savefig(target / filename, dpi=160)
        plt.close(fig)
    return best
