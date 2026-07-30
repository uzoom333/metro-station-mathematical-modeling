"""Illustrative reconstruction of a metro-station temperature model.

This file was newly written for this repository after the competition. It is
not recovered or adapted original 2024 competition code. The original
equations, algorithm, code, and numerical values are unavailable here. Every
function, formula, numerical method, and numerical value below is illustrative
and must not be attributed to the awarded submission.

The prototype uses only the Python standard library.
"""


def passenger_heat(passenger_count, heat_per_passenger_w):
    """Return illustrative passenger sensible heat in watts."""
    return passenger_count * heat_per_passenger_w


def train_heat(time_s, arrival_s, departure_s, heat_output_w):
    """Return the reconstruction's illustrative train heat source."""
    if arrival_s <= time_s < departure_s:
        return heat_output_w
    return 0.0


def ventilation_heat_loss(
    station_temperature_c,
    outside_temperature_c,
    air_density_kg_m3,
    air_specific_heat_j_kg_k,
    airflow_m3_s,
):
    """Return illustrative heat removed by ventilation in watts.

    A negative result means that ventilation adds heat because the outside air
    is warmer than the station air.
    """
    temperature_difference = station_temperature_c - outside_temperature_c
    return (
        air_density_kg_m3
        * air_specific_heat_j_kg_k
        * airflow_m3_s
        * temperature_difference
    )


def temperature_rate(
    time_s,
    station_temperature_c,
    passenger_count,
    heat_per_passenger_w,
    train_arrival_s,
    train_departure_s,
    train_heat_output_w,
    outside_temperature_c,
    station_volume_m3,
    air_density_kg_m3,
    air_specific_heat_j_kg_k,
    airflow_m3_s,
):
    """Return the illustrative station temperature rate in degrees C/second."""
    heat_from_passengers = passenger_heat(
        passenger_count, heat_per_passenger_w
    )
    heat_from_train = train_heat(
        time_s, train_arrival_s, train_departure_s, train_heat_output_w
    )
    heat_removed = ventilation_heat_loss(
        station_temperature_c,
        outside_temperature_c,
        air_density_kg_m3,
        air_specific_heat_j_kg_k,
        airflow_m3_s,
    )

    thermal_capacity = (
        air_density_kg_m3 * air_specific_heat_j_kg_k * station_volume_m3
    )
    net_heat_w = heat_from_passengers + heat_from_train - heat_removed
    return net_heat_w / thermal_capacity


def simulate(initial_temperature_c, duration_s, time_step_s, parameters):
    """Simulate the illustrative balance with the explicit Euler method."""
    time_s = 0.0
    temperature_c = initial_temperature_c
    samples = [(time_s, temperature_c)]

    while time_s < duration_s:
        step_s = min(time_step_s, duration_s - time_s)
        rate_c_s = temperature_rate(
            time_s=time_s,
            station_temperature_c=temperature_c,
            **parameters,
        )
        temperature_c += step_s * rate_c_s
        time_s += step_s
        samples.append((time_s, temperature_c))

    return samples


def main():
    # These values were selected for this repository only. They are not
    # recovered, estimated, or adapted values from the award-winning 2024
    # submission, and the output must not be presented as an original result.
    parameters = {
        "passenger_count": 100,
        "heat_per_passenger_w": 100.0,
        "train_arrival_s": 10.0 * 60.0,
        "train_departure_s": 12.0 * 60.0,
        "train_heat_output_w": 50_000.0,
        "outside_temperature_c": 24.0,
        "station_volume_m3": 20_000.0,
        "air_density_kg_m3": 1.2,
        "air_specific_heat_j_kg_k": 1_005.0,
        "airflow_m3_s": 20.0,
    }

    samples = simulate(
        initial_temperature_c=26.0,
        duration_s=30.0 * 60.0,
        time_step_s=10.0,
        parameters=parameters,
    )

    print("Repository-created illustration — not original equations or results")
    print("Time (min) | Station temperature (°C)")
    print("-" * 38)
    for time_s, temperature_c in samples:
        if time_s % 300 == 0:
            print(f"{time_s / 60:10.0f} | {temperature_c:24.2f}")


if __name__ == "__main__":
    main()
