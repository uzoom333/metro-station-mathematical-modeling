"""Shared low-order physical calculations."""

from __future__ import annotations

import math

from .constants import (
    AIR_CV_J_PER_KG_K,
    AIR_MOLAR_MASS_KG_PER_MOL,
    AIR_SPECIFIC_GAS_CONSTANT_J_PER_KG_K,
)


def air_properties(
    mass_kg: float, energy_j: float, volume_m3: float
) -> dict[str, float]:
    """Calculate temperature, pressure, density, and total air moles."""
    if mass_kg <= 0 or energy_j <= 0 or volume_m3 <= 0:
        raise ValueError("Air state must have positive mass, energy, and volume")
    temperature_k = energy_j / (mass_kg * AIR_CV_J_PER_KG_K)
    if temperature_k <= 0:
        raise ValueError("Air temperature must be positive")
    return {
        "temperature_k": temperature_k,
        "pressure_pa": mass_kg
        * AIR_SPECIFIC_GAS_CONSTANT_J_PER_KG_K
        * temperature_k
        / volume_m3,
        "density_kg_m3": mass_kg / volume_m3,
        "moles": mass_kg / AIR_MOLAR_MASS_KG_PER_MOL,
    }


def leakage_airflow(delta_pressure_pa: float, coefficient: float) -> float:
    """Return signed leakage; positive is outward and negative is inward."""
    if coefficient < 0:
        raise ValueError("Leakage coefficient cannot be negative")
    if delta_pressure_pa == 0:
        return 0.0
    return coefficient * math.copysign(
        math.sqrt(abs(delta_pressure_pa)), delta_pressure_pa
    )


def fan_power_proxy(
    flow_m3_s: float, reference_power_w: float, reference_flow: float
) -> float:
    """Return an illustrative cubic fan-power proxy."""
    if flow_m3_s < 0 or reference_power_w < 0 or reference_flow <= 0:
        raise ValueError("Fan proxy inputs must be physical")
    return reference_power_w * (flow_m3_s / reference_flow) ** 3
