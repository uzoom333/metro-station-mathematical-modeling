# Assumptions

## Status of this document

The list below defines assumptions chosen now for the repository's illustrative
reconstruction. It is informed by broad remembered topics from the 2024
project, but there is no complete surviving record showing which assumptions
the original team used or how they stated them. None of the specific
assumptions below should be attributed to the awarded submission.

## Assumptions selected for the reconstruction

1. **One hypothetical station:** the model represents a single enclosed station
   volume rather than an entire metro network.
2. **Well-mixed air:** at each instant, the station air is represented by one
   average temperature. Local hot spots and spatial gradients are omitted.
3. **Minimum passenger population:** a fixed minimum number of passengers is
   present during the modeled period. Passenger arrivals and departures are
   simplified.
4. **Passenger heat:** each passenger contributes heat at an average rate.
5. **Train heat:** a train contributes heat while it is in or near the station.
   The source may be represented by a simple time-dependent function.
6. **Ventilation airflow:** outside air enters and station air leaves at
   equivalent average flow rates, so air volume is conserved.
7. **Known station volume:** the station is assigned a constant effective air
   volume.
8. **Known outside temperature:** outside-air temperature is treated as fixed
   in the simplest prototype.
9. **Constant air properties:** air density and specific heat are treated as
   constants.
10. **Other heat paths omitted:** conduction through walls, solar gains,
    humidity, equipment heat, tunnel piston effects, and detailed train
    aerodynamics are not represented in Version 1.

The list above describes only the model implemented in this repository. The
numerical choices used in the Python prototype were also selected now to make
the reconstruction runnable. They are not recovered or estimated values from
the competition entry.
