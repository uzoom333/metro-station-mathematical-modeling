"""Unit conversions with SI units used internally."""

from .constants import UNIVERSAL_GAS_CONSTANT_J_PER_MOL_K


def celsius_to_kelvin(value_c: float) -> float:
    """Convert degrees Celsius to kelvin."""
    return value_c + 273.15


def kelvin_to_celsius(value_k: float) -> float:
    """Convert kelvin to degrees Celsius."""
    return value_k - 273.15


def ppm_to_mole_fraction(ppm: float) -> float:
    """Convert parts per million to mole fraction."""
    return ppm * 1.0e-6


def mole_fraction_to_ppm(fraction: float) -> float:
    """Convert mole fraction to parts per million."""
    return fraction * 1.0e6


def liters_per_second_to_moles_per_second(
    flow_l_s: float, pressure_pa: float, temperature_k: float
) -> float:
    """Convert ideal-gas volumetric flow to molar flow."""
    if temperature_k <= 0 or pressure_pa <= 0 or flow_l_s < 0:
        raise ValueError("CO2 conversion inputs must be physical")
    flow_m3_s = flow_l_s * 1.0e-3
    return (
        pressure_pa * flow_m3_s / (UNIVERSAL_GAS_CONSTANT_J_PER_MOL_K * temperature_k)
    )
