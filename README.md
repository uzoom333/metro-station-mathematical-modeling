# Metro Station Mathematical Modeling

This repository documents the evolution of a mathematical modeling project
developed in 2024 for the Mathematical Modeling Challenge at PUC Goiás, where
the original project received fourth place.

What is currently remembered about the awarded project is limited to its broad
scope: it considered thermal and ventilation conditions in one hypothetical
metro station; a minimum passenger population; heat from passengers and a
train; airflow; temperature; station volume; and multiple differential
equations. The challenge emphasized logical reasoning, assumption definition,
and mathematical problem decomposition rather than a complete or
construction-ready engineering solution. This summary does not establish the
original equations, parameter values, diagrams, or implementation.

## Versions

### Version 1: Original-model reconstruction

[`original-model/`](original-model/) is a careful reconstruction based on
details currently remembered about the 2024 project. Some original equations,
numerical values, and drawings are no longer available. Consequently:

- the reconstruction is not a verbatim copy of the awarded submission;
- all equations, notation, numerical values, algorithms, and Python code in
  this repository are newly created illustrative material unless surviving
  evidence is explicitly cited; and
- none of that illustrative material is claimed to have appeared in or
  contributed to the awarded submission.

### Version 2: Remodeled model

[`remodeled-model/`](remodeled-model/) is reserved for a future expansion using
modern numerical simulation and software engineering practices. It will remain
separate from Version 1 so that later improvements are not confused with the
historical reconstruction.

## Repository layout

```text
.
├── README.md
├── original-model/
│   ├── README.md
│   ├── assumptions.md
│   ├── equations.md
│   ├── limitations.md
│   └── original_reconstruction.py
├── remodeled-model/
│   └── README.md
├── LICENSE
└── .gitignore
```

## Running the prototype

The repository-created Version 1 prototype uses only the Python standard
library:

```bash
python3 original-model/original_reconstruction.py
```

The program was written for this repository after the competition. It is an
educational illustration of one possible reconstruction, not recovered
competition code. Its output is not an original competition result or a
validated engineering prediction.

## License

This repository is available under the [MIT License](LICENSE).
