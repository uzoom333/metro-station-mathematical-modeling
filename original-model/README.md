# Version 1: Original-Model Reconstruction

This directory contains a new reconstruction informed only by broad details
currently remembered about the 2024 competition project. The original project,
which received fourth place in the Mathematical Modeling Challenge at PUC
Goiás, concerned thermal and ventilation conditions in one hypothetical metro
station. That award applies to the 2024 project, not to the reconstruction,
documentation, equations, or code in this repository.

This repository version is intentionally simple. It follows the challenge's
remembered educational emphasis by defining assumptions, identifying relevant
quantities, and demonstrating one way to decompose heat and airflow concepts.
The particular decomposition and mathematical implementation documented here
are present-day reconstruction choices.

It is not an archival reproduction. The original equations, parameter values,
drawings, and code are not available here. Unless a future source is explicitly
cited, every equation, symbol, parameter value, numerical method, and line of
code in this directory must be treated as newly created illustrative material
and must not be attributed to the awarded submission.

## Files

- [`assumptions.md`](assumptions.md) records assumptions selected for this
  reconstruction.
- [`equations.md`](equations.md) describes likely equation families and gives
  one explicitly illustrative formulation.
- [`limitations.md`](limitations.md) defines historical and technical limits.
- [`original_reconstruction.py`](original_reconstruction.py) implements a small,
  dependency-free prototype written for this repository, not recovered
  competition code.

Run the prototype from the repository root:

```bash
python3 original-model/original_reconstruction.py
```
