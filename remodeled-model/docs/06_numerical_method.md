# Numerical Method

SciPy `solve_ivp` integrates the coupled system with RK45, relative tolerance
\(10^{-7}\), absolute tolerance \(10^{-9}\), and a deterministic five-second
output grid. A failed solver raises an error. Post-processing rejects NaN,
infinity, nonpositive mass, and nonpositive absolute temperature.

Trapezoidal integration calculates heat, fan energy, and time above selected
analysis thresholds. Discontinuous schedule events and the square-root leakage
law are retained explicitly; the tolerances are therefore important.
