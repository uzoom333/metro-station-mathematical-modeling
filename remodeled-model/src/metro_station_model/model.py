"""Coupled differential equations for the Version 2 model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .constants import (
    AIR_CP_J_PER_KG_K,
    AIR_MOLAR_MASS_KG_PER_MOL,
    AIR_SPECIFIC_GAS_CONSTANT_J_PER_KG_K,
)
from .controller import ventilation_target
from .conversions import (
    celsius_to_kelvin,
    liters_per_second_to_moles_per_second,
    mole_fraction_to_ppm,
    ppm_to_mole_fraction,
)
from .physics import air_properties, leakage_airflow
from .schedules import passenger_count, piston_airflow, train_heat, train_present


@dataclass(frozen=True)
class Evaluation:
    """ODE derivatives and diagnostics evaluated at one instant."""

    derivative: NDArray[np.float64]
    diagnostics: dict[str, float | bool]


def initial_state(config: dict) -> NDArray[np.float64]:
    """Build a thermodynamically consistent initial state."""
    station = config["station"]
    initial = config["initial_conditions"]
    temperature_k = celsius_to_kelvin(initial["air_temperature_C"])
    mass = (
        initial["pressure_Pa"]
        * station["volume_m3"]
        / (AIR_SPECIFIC_GAS_CONSTANT_J_PER_KG_K * temperature_k)
    )
    from .constants import AIR_CV_J_PER_KG_K

    energy = mass * AIR_CV_J_PER_KG_K * temperature_k
    moles_air = mass / AIR_MOLAR_MASS_KG_PER_MOL
    co2_moles = ppm_to_mole_fraction(initial["co2_ppm"]) * moles_air
    return np.array(
        [
            mass,
            energy,
            celsius_to_kelvin(initial["structure_temperature_C"]),
            co2_moles,
            initial["ventilation_airflow_m3_s"],
        ],
        dtype=float,
    )


def evaluate(time_s: float, state: NDArray[np.float64], config: dict) -> Evaluation:
    """Evaluate all coupled balances without duplicating physical equations."""
    mass, energy, structure_k, co2_moles, ventilation_flow = state
    station = config["station"]
    thermal = config["thermal"]
    outdoor = config["outdoor"]
    occupancy = config["occupancy"]
    train = config["train"]
    vent = config["ventilation"]
    properties = air_properties(mass, energy, station["volume_m3"])
    air_k = properties["temperature_k"]
    pressure_pa = properties["pressure_pa"]
    density_inside = properties["density_kg_m3"]
    air_moles = properties["moles"]
    if co2_moles < 0 or co2_moles > air_moles:
        raise ValueError("CO2 mole fraction must be between zero and one")
    co2_fraction = co2_moles / air_moles
    co2_ppm = mole_fraction_to_ppm(co2_fraction)
    outdoor_k = celsius_to_kelvin(outdoor["temperature_C"])
    density_outdoor = outdoor["pressure_Pa"] / (
        AIR_SPECIFIC_GAS_CONSTANT_J_PER_KG_K * outdoor_k
    )

    passengers = passenger_count(
        time_s, occupancy["schedule"], occupancy["minimum_passengers"]
    )
    passenger_heat_w = passengers * thermal["passenger_sensible_heat_W_per_person"]
    train_heat_w = train_heat(
        time_s,
        train["arrival_times_s"],
        train["dwell_time_s"],
        train["direct_heat_W"],
        train["residual_heat_initial_W"],
        train["residual_decay_time_s"],
    )
    piston_flow = piston_airflow(
        time_s,
        train["arrival_times_s"],
        train["dwell_time_s"],
        train["piston_event_duration_s"],
        train["piston_airflow_m3_s"],
    )
    target_flow = ventilation_target(time_s, air_k, co2_ppm, vent, config["failure"])
    pressure_difference = pressure_pa - outdoor["pressure_Pa"]
    leak_signed = leakage_airflow(
        pressure_difference, vent["leakage_coefficient_m3_s_sqrt_Pa"]
    )
    leak_in = max(-leak_signed, 0.0)
    leak_out = max(leak_signed, 0.0)
    effective_ventilation = max(ventilation_flow, 0.0)
    total_volume_in = effective_ventilation + piston_flow + leak_in
    total_volume_out = effective_ventilation + piston_flow + leak_out
    mass_in = density_outdoor * total_volume_in
    mass_out = density_inside * total_volume_out

    d_mass = mass_in - mass_out
    d_energy = (
        passenger_heat_w
        + train_heat_w
        + thermal["equipment_heat_W"]
        + thermal["air_structure_conductance_W_per_K"] * (structure_k - air_k)
        + mass_in * AIR_CP_J_PER_KG_K * outdoor_k
        - mass_out * AIR_CP_J_PER_KG_K * air_k
    )
    d_structure = (
        thermal["air_structure_conductance_W_per_K"] * (air_k - structure_k)
        + thermal["structure_outdoor_UA_W_per_K"] * (outdoor_k - structure_k)
    ) / thermal["structure_thermal_capacitance_J_per_K"]
    generation = passengers * liters_per_second_to_moles_per_second(
        config["air_quality"]["passenger_co2_generation_L_per_s_person"],
        outdoor["pressure_Pa"],
        config["air_quality"]["conversion_reference_temperature_K"],
    )
    d_co2 = (
        ppm_to_mole_fraction(config["air_quality"]["outdoor_co2_ppm"])
        * mass_in
        / AIR_MOLAR_MASS_KG_PER_MOL
        - co2_fraction * mass_out / AIR_MOLAR_MASS_KG_PER_MOL
        + generation
    )
    d_ventilation = (target_flow - effective_ventilation) / vent[
        "actuator_time_constant_s"
    ]
    diagnostics: dict[str, float | bool] = {
        "passengers": passengers,
        "train_present": train_present(
            time_s, train["arrival_times_s"], train["dwell_time_s"]
        ),
        "passenger_heat_W": passenger_heat_w,
        "train_heat_W": train_heat_w,
        "equipment_heat_W": thermal["equipment_heat_W"],
        "piston_airflow_m3_s": piston_flow,
        "target_ventilation_airflow_m3_s": target_flow,
        "leakage_airflow_signed_m3_s": leak_signed,
        "total_mass_inflow_kg_s": mass_in,
        "total_mass_outflow_kg_s": mass_out,
        "air_density_kg_m3": density_inside,
        "air_temperature_K": air_k,
        "internal_pressure_Pa": pressure_pa,
        "pressure_difference_Pa": pressure_difference,
        "co2_ppm": co2_ppm,
    }
    return Evaluation(
        np.array([d_mass, d_energy, d_structure, d_co2, d_ventilation]),
        diagnostics,
    )


def derivatives(
    time_s: float, state: NDArray[np.float64], config: dict
) -> NDArray[np.float64]:
    """Return the Version 2 state derivative."""
    return evaluate(time_s, state, config).derivative
