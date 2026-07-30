"""Passenger and train schedules."""

from __future__ import annotations

import math

import numpy as np


def passenger_count(
    time_s: float, schedule: list[list[float]], minimum: float
) -> float:
    """Evaluate a piecewise-linear occupancy schedule."""
    times = np.asarray([point[0] for point in schedule], dtype=float)
    values = np.asarray([point[1] for point in schedule], dtype=float)
    return float(max(minimum, np.interp(time_s, times, values)))


def train_present(time_s: float, arrivals: list[float], dwell_s: float) -> bool:
    """Return whether any train is in its dwell interval."""
    return any(arrival <= time_s < arrival + dwell_s for arrival in arrivals)


def train_heat(
    time_s: float,
    arrivals: list[float],
    dwell_s: float,
    direct_w: float,
    residual_w: float,
    decay_s: float,
) -> float:
    """Sum direct dwell heat and post-departure exponential residual heat."""
    total = 0.0
    for arrival in arrivals:
        departure = arrival + dwell_s
        if arrival <= time_s < departure:
            total += direct_w
        elif time_s >= departure:
            total += residual_w * math.exp(-(time_s - departure) / decay_s)
    return total


def piston_airflow(
    time_s: float, arrivals: list[float], dwell_s: float, duration_s: float, flow: float
) -> float:
    """Return train exchange during windows centered on arrival and departure.

    Each window begins half an event duration before the event and ends half an
    event duration after it. Overlapping events contribute only one configured
    bidirectional exchange rate.
    """
    half = duration_s / 2.0
    events = [event for arrival in arrivals for event in (arrival, arrival + dwell_s)]
    return (
        flow if any(event - half <= time_s < event + half for event in events) else 0.0
    )
