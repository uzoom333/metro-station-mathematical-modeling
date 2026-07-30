# Engineering Assumptions

The original project used engineering assumptions to reduce a complex metro
station to a mathematical system suitable for analysis with Differential
Equations and Calculus II. The assumptions preserved in Version 1 are:

1. **Single hypothetical station:** the model covers one station rather than an
   entire metro network.
2. **Defined station volume:** the station has a finite air volume used in the
   thermal and ventilation balances.
3. **Minimum passenger occupancy:** a minimum number of passengers is present
   in the modeled station.
4. **Passenger heat generation:** passengers contribute heat to the station.
5. **Train heat generation:** an arriving train adds heat to the station
   environment.
6. **Airflow and air renewal:** ventilation replaces station air and affects
   its thermal conditions.
7. **Interacting quantities:** passenger heat, train heat, airflow, volume, and
   temperature must be considered together rather than as isolated effects.
8. **Simplified engineering system:** the hypothetical station is simplified
   enough to support logical decomposition and coupled differential equations.

## Use in the Repository Example

The Python example makes additional computational choices—such as a
well-mixed-air approximation, constant air properties, constant outside
temperature, balanced airflow, and a time window for train presence—to express
the preserved assumptions in runnable form. Those implementation choices, as
well as all numerical values and station dimensions in the example, are
illustrative replacements rather than recovered historical details.
