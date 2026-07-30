# Scope and Limitations

## Original Project Scope

The project was created for a mathematical modeling challenge. Its purpose was
to demonstrate logical reasoning, sound assumptions, mathematical
decomposition, and the use of coupled differential equations to represent the
ventilation and thermal conditions of a hypothetical metro station.

It was not intended to provide a complete engineering design, certify a
ventilation system, or establish operational and safety requirements for a real
station.

## Version 1 Computational Limitations

The current Python example translates the preserved modeling approach into a
small, readable simulation. For that purpose, it:

- represents the station as one well-mixed air volume;
- omits spatial temperature and airflow distributions;
- simplifies passenger and train behavior;
- omits humidity, radiation, wall conduction, equipment loads, solar gains,
  leakage, and detailed tunnel effects;
- uses constant air properties, outside temperature, and airflow;
- uses recreated parameters that have not been calibrated against
  measurements;
- uses a basic Euler integrator without automatic error or stability control;
  and
- includes no sensitivity, uncertainty, or validation study.

These computational limitations describe the repository example, not
additional claims about the 2024 submission. The example is suitable for
explaining the mathematical structure, but not for engineering decisions.

Version 2 may address these limitations with sourced parameters, configurable
scenarios, tested numerical methods, uncertainty analysis, validation, and
modern software engineering practices.
