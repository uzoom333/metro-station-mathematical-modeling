"""Configuration validation tests."""

from copy import deepcopy
from pathlib import Path

import pytest

from metro_station_model.config import load_config, validate_config

CONFIGS = Path(__file__).parents[1] / "configs"


def test_all_configurations_resolve_with_required_metadata() -> None:
    for path in CONFIGS.glob("*.yaml"):
        config = load_config(path)
        assert config.data["metadata"]["data_status"] == "synthetic_illustrative"
        assert config.data["metadata"]["engineering_validation"] is False
        assert config.data["metadata"]["original_submission_data"] is False


def test_geometry_must_match_volume() -> None:
    data = deepcopy(load_config(CONFIGS / "baseline.yaml").data)
    data["station"]["volume_m3"] += 1
    with pytest.raises(ValueError, match="multiply"):
        validate_config(data)


def test_airflow_limits_must_be_ordered() -> None:
    data = deepcopy(load_config(CONFIGS / "baseline.yaml").data)
    data["ventilation"]["minimum_airflow_m3_s"] = 101
    with pytest.raises(ValueError, match="limits"):
        validate_config(data)


def test_invalid_schedule_is_rejected() -> None:
    data = deepcopy(load_config(CONFIGS / "baseline.yaml").data)
    data["occupancy"]["schedule"] = [[10, 4], [0, 4]]
    with pytest.raises(ValueError, match="schedule"):
        validate_config(data)
