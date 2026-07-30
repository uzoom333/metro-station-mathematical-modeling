# Sensitivity Analysis

The analysis includes 50 one-at-a-time runs and 500 uniform Latin-hypercube
samples with seed 2024. Input ranges are defined in `sensitivity.py` and all
samples are saved.

The strongest absolute Spearman relations were:

- maximum temperature vs outdoor temperature: 0.979;
- maximum pressure deviation vs leakage coefficient: -0.793;
- fan-energy proxy vs outdoor temperature: 0.760;
- fan-energy proxy vs base airflow: 0.671.

These model-specific rank correlations show association, not causation or
real-world sensitivity.

![Rank correlations](../results/sensitivity/rank_correlation_heatmap.png)
