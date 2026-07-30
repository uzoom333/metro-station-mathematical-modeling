# Version 1: Original Model

Version 1 faithfully reconstructs the mathematical modeling project that
received fourth place in the Mathematical Modeling Challenge at the X Congress
of Science, Technology and Innovation at PUC Goiás in 2024.

## Problem

The project considered one hypothetical metro station and asked how its
ventilation and thermal conditions could be represented mathematically. The
system combined human occupancy, a train entering the station, air renewal,
temperature, and the finite volume of the station.

## Modeling Methodology

The original reasoning followed a clear undergraduate mathematical-modeling
workflow:

1. define the station as the system under study;
2. state engineering assumptions that make the problem tractable;
3. identify the principal variables and heat sources;
4. express how those variables change and interact through Differential
   Equations and Calculus II;
5. connect the equations as a coupled model; and
6. interpret the model as a logical representation of ventilation and thermal
   behavior.

This methodology reflects the competition's focus on assumptions, reasoning,
and problem decomposition rather than delivery of a complete engineering
design.

## Contents

- [`assumptions.md`](assumptions.md) presents the engineering assumptions
  preserved from the project.
- [`equations.md`](equations.md) explains the preserved mathematical approach
  and labels the displayed formulation as illustrative.
- [`limitations.md`](limitations.md) defines the intended academic scope.
- [`original_reconstruction.py`](original_reconstruction.py) is a newly
  developed computational example using recreated parameter values.

The precise numerical values, dimensions, historical diagrams, and original
implementation are not available. Examples that replace those details are
identified where they appear.

Run the example from the repository root:

```bash
python3 original-model/original_reconstruction.py
```
