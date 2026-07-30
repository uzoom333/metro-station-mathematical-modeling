"""Conversion and state-consistency tests."""

from pathlib import Path

import pytest

from metro_station_model.config import load_config
from metro_station_model.conversions import (
    celsius_to_kelvin,
    kelvin_to_celsius,
    liters_per_second_to_moles_per_second,
    mole_fraction_to_ppm,
    ppm_to_mole_fraction,
)
from metro_station_model.validation import co2_round_trip_ppm

CONFIG = load_config(Path(__file__).parents[1] / "configs/baseline.yaml")


def test_temperature_round_trip() -> None:
    assert kelvin_to_celsius(celsius_to_kelvin(26.0)) == pytest.approx(26.0)


def test_ppm_fraction_round_trip() -> None:
    assert mole_fraction_to_ppm(ppm_to_mole_fraction(600.0)) == pytest.approx(600.0)
    assert co2_round_trip_ppm(CONFIG.data) == pytest.approx(600.0)


def test_volumetric_co2_conversion_is_positive() -> None:
    value = liters_per_second_to_moles_per_second(0.004, 101325, 298.15)
    assert value > 0


def test_nonphysical_conversion_rejected() -> None:
    with pytest.raises(ValueError):
        liters_per_second_to_moles_per_second(0.004, 101325, 0)
