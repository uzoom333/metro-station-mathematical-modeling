# Equation Types and Illustrative Reconstruction

## Historical scope

It is remembered that the project involved multiple differential equations and
quantities such as passenger heat, train heat, airflow, temperature, and
station volume. The original equations, notation, and numerical method are not
available here. The equation families below are present-day conjectures about
what such a model could use. They are not evidence of what the awarded
submission actually used.

Possible equation families for a new reconstruction include:

- an energy balance for the station air;
- source terms for heat released by passengers and a train;
- a ventilation or air-volume balance;
- temperature change expressed as an ordinary differential equation; and
- time-dependent rules for train presence or other operating conditions.

## Illustrative formulation

**Everything from this point onward—including every symbol, equation,
relationship, and numerical method—was selected for this repository as an
illustrative reconstruction. None of it is claimed to have been used in the
2024 submission or to have contributed to its award.**

Let:

- \(T(t)\) be the average station-air temperature in degrees Celsius;
- \(T_{\text{out}}\) be the outside-air temperature;
- \(V\) be the effective station-air volume;
- \(\rho\) be air density;
- \(c_p\) be the specific heat capacity of air;
- \(\dot V\) be the ventilation volumetric flow rate;
- \(N\) be the modeled passenger count;
- \(q_p\) be the average sensible heat released per passenger; and
- \(Q_{\text{train}}(t)\) be a time-dependent train heat source.

An illustrative passenger heat source is

\[
Q_{\text{passengers}} = N q_p.
\]

For balanced ventilation, an illustrative heat-removal term is

\[
Q_{\text{ventilation}}
  = \rho c_p \dot V \left(T(t) - T_{\text{out}}\right).
\]

Combining these terms in a lumped energy balance gives the illustrative
ordinary differential equation

\[
\rho c_p V \frac{dT}{dt}
  = Q_{\text{passengers}}
  + Q_{\text{train}}(t)
  - Q_{\text{ventilation}}.
\]

Equivalently,

\[
\frac{dT}{dt}
  =
  \frac{
    Nq_p + Q_{\text{train}}(t)
    - \rho c_p \dot V(T-T_{\text{out}})
  }{\rho c_p V}.
\]

The repository-created prototype evaluates this equation with the explicit
Euler method. There is no surviving evidence that the original submission used
this method:

\[
T_{k+1} = T_k + \Delta t\, f(t_k, T_k).
\]

Within this new illustrative formulation, internal sources warm the air while
ventilation tends to move station temperature toward outside temperature. This
observation explains the reconstruction only; it does not describe a recovered
original result. The formulation is not a validated design model.
