# Software Architecture

`config` resolves and validates YAML; `schedules` evaluates occupancy and train
events; `controller` determines airflow targets; `physics` provides shared
relations; `model` is the single source of coupled derivatives; `solver`
integrates and builds the DataFrame; `metrics` summarizes it; `results` and
`plotting` persist artifacts; `scenarios`, `sensitivity`, and `optimization`
orchestrate experiments; and `cli` exposes workflows.

No model equation is duplicated in analysis modules.
