# Validation

Automated checks cover geometry, ranges, schedules, controller clipping,
initial ideal-gas pressure, CO₂ round trip, solver success, finite/physical
states, deterministic repetition, all scenarios, and mass-balance integration.

Two isolated benchmarks compare `solve_ivp` with analytical first-order
solutions:

$$
C(t)=C_o+(C_0-C_o)e^{-kt},\qquad
T(t)=T_\infty+(T_0-T_\infty)e^{-kt}
$$

The no-source equilibrium test sets air, structure, and outdoor conditions
equal and confirms an approximately constant state. Passing these tests checks
implementation behavior; it does not validate the model for a real station.
