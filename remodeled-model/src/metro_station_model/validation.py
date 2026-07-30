"""Validation helpers and analytical benchmarks."""

from __future__ import annotations

import numpy as np

from .constants import (
    AIR_MOLAR_MASS_KG_PER_MOL,
    AIR_SPECIFIC_GAS_CONSTANT_J_PER_KG_K,
)
from .conversions import mole_fraction_to_ppm
from .model import initial_state


def initial_pressure_error_pa(config: dict) -> float:
    """Return ideal-gas consistency error for the generated initial state."""
    state = initial_state(config)
    mass, energy = state[:2]
    from .constants import AIR_CV_J_PER_KG_K

    temperature = energy / (mass * AIR_CV_J_PER_KG_K)
    pressure = (
        mass
        * AIR_SPECIFIC_GAS_CONSTANT_J_PER_KG_K
        * temperature
        / config["station"]["volume_m3"]
    )
    return float(pressure - config["initial_conditions"]["pressure_Pa"])


def co2_round_trip_ppm(config: dict) -> float:
    """Recover initial CO2 ppm through fraction, moles, and air moles."""
    state = initial_state(config)
    air_moles = state[0] / AIR_MOLAR_MASS_KG_PER_MOL
    fraction = state[3] / air_moles
    return mole_fraction_to_ppm(fraction)


def analytical_mixed_concentration(
    time_s: np.ndarray, initial: float, outdoor: float, exchange_rate_s: float
) -> np.ndarray:
    """Return the first-order constant-flow concentration solution."""
    return outdoor + (initial - outdoor) * np.exp(-exchange_rate_s * time_s)


def analytical_first_order_temperature(
    time_s: np.ndarray, initial_k: float, equilibrium_k: float, rate_s: float
) -> np.ndarray:
    """Return a first-order exponential thermal solution."""
    return equilibrium_k + (initial_k - equilibrium_k) * np.exp(-rate_s * time_s)
