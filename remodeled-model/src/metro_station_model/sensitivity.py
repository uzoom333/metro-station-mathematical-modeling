"""Deterministic one-at-a-time and Latin-hypercube experiments."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import qmc

from .config import ModelConfig
from .metrics import summary_metrics
from .solver import simulate

PARAMETER_RANGES = {
    "station_volume_m3": (0.8, 1.2),  # factors applied to baseline
    "passenger_heat_W_per_person": (60.0, 100.0),
    "passenger_co2_L_s_person": (0.003, 0.006),
    "train_direct_heat_W": (150000.0, 400000.0),
    "structure_outdoor_UA_W_K": (3000.0, 8000.0),
    "structure_capacitance_J_K": (800000000.0, 2000000000.0),
    "base_airflow_m3_s": (15.0, 40.0),
    "maximum_airflow_m3_s": (60.0, 120.0),
    "leakage_coefficient": (0.15, 0.60),
    "outdoor_temperature_C": (28.0, 36.0),
}

OUTPUTS = [
    "maximum_air_temperature_C",
    "maximum_co2_ppm",
    "maximum_absolute_pressure_difference_Pa",
    "total_fan_energy_proxy_kWh",
]


def _set_parameter(data: dict, name: str, value: float, baseline_volume: float) -> None:
    paths = {
        "passenger_heat_W_per_person": (
            "thermal",
            "passenger_sensible_heat_W_per_person",
        ),
        "passenger_co2_L_s_person": (
            "air_quality",
            "passenger_co2_generation_L_per_s_person",
        ),
        "train_direct_heat_W": ("train", "direct_heat_W"),
        "structure_outdoor_UA_W_K": ("thermal", "structure_outdoor_UA_W_per_K"),
        "structure_capacitance_J_K": (
            "thermal",
            "structure_thermal_capacitance_J_per_K",
        ),
        "base_airflow_m3_s": ("ventilation", "base_airflow_m3_s"),
        "maximum_airflow_m3_s": ("ventilation", "maximum_airflow_m3_s"),
        "leakage_coefficient": (
            "ventilation",
            "leakage_coefficient_m3_s_sqrt_Pa",
        ),
        "outdoor_temperature_C": ("outdoor", "temperature_C"),
    }
    if name == "station_volume_m3":
        volume = baseline_volume * value
        data["station"]["volume_m3"] = volume
        data["station"]["length_m"] = volume / (
            data["station"]["width_m"] * data["station"]["average_height_m"]
        )
        return
    section, key = paths[name]
    data[section][key] = value
    if name == "base_airflow_m3_s":
        data["ventilation"]["maximum_airflow_m3_s"] = max(
            value, data["ventilation"]["maximum_airflow_m3_s"]
        )


def _variant(config: ModelConfig, name: str, value: float) -> ModelConfig:
    data = deepcopy(config.data)
    _set_parameter(data, name, value, config.data["station"]["volume_m3"])
    return ModelConfig(data, config.source)


def run_oat(config: ModelConfig) -> pd.DataFrame:
    """Run five deterministic levels for each configured parameter range."""
    rows = []
    for name, (low, high) in PARAMETER_RANGES.items():
        for level, value in enumerate(np.linspace(low, high, 5)):
            metrics = summary_metrics(simulate(_variant(config, name, float(value))))
            rows.append({"parameter": name, "level": level, "value": value, **metrics})
    return pd.DataFrame(rows)


def run_latin_hypercube(config: ModelConfig, samples: int = 500) -> pd.DataFrame:
    """Run a seeded uniform Latin-hypercube experiment."""
    if samples <= 0:
        raise ValueError("Sample count must be positive")
    names = list(PARAMETER_RANGES)
    lower = np.array([PARAMETER_RANGES[name][0] for name in names])
    upper = np.array([PARAMETER_RANGES[name][1] for name in names])
    seed = int(config.data["simulation"]["random_seed"])
    values = qmc.scale(
        qmc.LatinHypercube(len(names), seed=seed).random(samples), lower, upper
    )
    rows = []
    for sample_index, sample in enumerate(values):
        data = deepcopy(config.data)
        for name, value in zip(names, sample, strict=True):
            _set_parameter(
                data, name, float(value), config.data["station"]["volume_m3"]
            )
        metrics = summary_metrics(simulate(ModelConfig(data, config.source)))
        rows.append(
            {"sample": sample_index, **dict(zip(names, sample, strict=True)), **metrics}
        )
    return pd.DataFrame(rows)


def save_sensitivity(
    oat: pd.DataFrame, lhs: pd.DataFrame, directory: str | Path
) -> pd.DataFrame:
    """Save tables and normalized sensitivity visualizations."""
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    oat.to_csv(target / "one_at_a_time.csv", index=False)
    lhs.to_csv(target / "latin_hypercube.csv", index=False)
    ranks = (
        lhs[list(PARAMETER_RANGES) + OUTPUTS]
        .corr(method="spearman")
        .loc[list(PARAMETER_RANGES), OUTPUTS]
    )
    ranks.to_csv(target / "rank_correlations.csv")

    baseline = oat[oat["level"] == 2].set_index("parameter")
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    for output, axis in zip(OUTPUTS, axes.flat, strict=True):
        for parameter, group in oat.groupby("parameter"):
            reference = baseline.loc[parameter, output]
            normalized = (group[output] - reference) / max(abs(reference), 1.0e-12)
            axis.plot(np.linspace(-1, 1, 5), normalized, marker="o", label=parameter)
        axis.set(title=output.replace("_", " "), xlabel="Normalized range position")
        axis.axhline(0, color="black", linewidth=0.7)
    axes[0, 0].legend(fontsize=6, ncol=2)
    fig.tight_layout()
    fig.savefig(target / "oat_normalized.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for output, axis in zip(OUTPUTS, axes.flat, strict=True):
        axis.hist(lhs[output], bins=25)
        axis.set(title=output.replace("_", " "))
    fig.tight_layout()
    fig.savefig(target / "output_histograms.png", dpi=160)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(8, 6))
    image = axis.imshow(ranks.to_numpy(), cmap="coolwarm", vmin=-1, vmax=1)
    axis.set_xticks(range(len(OUTPUTS)), [name.replace("_", "\n") for name in OUTPUTS])
    axis.set_yticks(range(len(PARAMETER_RANGES)), list(PARAMETER_RANGES))
    fig.colorbar(image, ax=axis, label="Spearman rank correlation")
    fig.tight_layout()
    fig.savefig(target / "rank_correlation_heatmap.png", dpi=160)
    plt.close(fig)

    for output in OUTPUTS:
        parameter = ranks[output].abs().idxmax()
        fig, axis = plt.subplots(figsize=(6, 4))
        axis.scatter(lhs[parameter], lhs[output], s=10, alpha=0.6)
        axis.set(
            xlabel=parameter, ylabel=output, title=f"{output}: strongest rank relation"
        )
        fig.tight_layout()
        fig.savefig(target / f"scatter_{output}.png", dpi=160)
        plt.close(fig)
    return ranks
