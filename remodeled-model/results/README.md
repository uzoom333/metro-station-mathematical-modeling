# Generated Results

These directories contain deterministic outputs calculated by Version 2 from
synthetic, illustrative inputs:

- `baseline/`: baseline CSV, JSON, resolved YAML, metadata, and plots;
- `scenarios/`: all configured cases and cross-scenario comparisons;
- `sensitivity/`: one-at-a-time and seeded Latin-hypercube results; and
- `optimization/`: illustrative controller-grid results.

Run `python scripts/regenerate_all_results.py` from `remodeled-model/` to
replace generated files. The script preserves this README and limits deletion
to the four documented result directories.

The outputs are educational experiments, not validated engineering results.
