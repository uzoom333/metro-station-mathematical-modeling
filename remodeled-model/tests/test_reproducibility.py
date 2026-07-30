"""Deterministic reproducibility test."""

from copy import deepcopy
from pathlib import Path

import pandas.testing as pdt

from metro_station_model.config import ModelConfig, load_config
from metro_station_model.solver import simulate


def test_repeated_simulation_is_identical() -> None:
    baseline = load_config(Path(__file__).parents[1] / "configs/baseline.yaml")
    data = deepcopy(baseline.data)
    data["simulation"]["end_time_s"] = 120
    config = ModelConfig(data, baseline.source)
    pdt.assert_frame_equal(simulate(config).frame, simulate(config).frame)
