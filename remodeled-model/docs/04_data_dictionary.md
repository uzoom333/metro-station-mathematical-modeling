# Data Dictionary

| State/output | Unit | Meaning |
|---|---|---|
| `m_air` / `air_mass_kg` | kg | Station air mass |
| `U_air` | J | Air internal energy |
| `T_structure` | K | Effective structure temperature |
| `n_co2` | mol | CO₂ amount |
| `Q_ventilation` | m³/s | Mechanical airflow state |
| `air_temperature_K` | K | Derived air temperature |
| `internal_pressure_Pa` | Pa | Ideal-gas internal pressure |
| `co2_ppm` | ppm | CO₂ mole fraction for display |
| `piston_airflow_m3_s` | m³/s | Bidirectional train exchange |
| `fan_power_proxy_W` | W | Illustrative cubic energy proxy |

All equation inputs use SI units. Celsius, ppm, minutes, kWh, and air changes
per hour are display/post-processing units.
