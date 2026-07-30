# References

These authoritative sources support general numerical and physical concepts;
they do not validate the synthetic station parameters.

1. [SciPy `solve_ivp` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)
   documents the initial-value solver and RK45 method used here.
2. NASA Glenn, [Equation of State](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/equation-of-state/),
   explains the ideal-gas relationship.
3. NASA Glenn, [Air Properties Definitions](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/air-properties-definitions/),
   defines pressure, density, and temperature relationships.
4. NIST, [Standard Reference Database 72](https://www.nist.gov/publications/nist-standard-reference-database-72-nist-thermophysical-properties-air-and-air),
   is an authoritative air-property resource; V2 instead uses constant
   approximate properties.
5. ASHRAE, [Standard 62.1 purpose and scope](https://www.ashrae.org/technical-resources/standards-and-guidelines/titles-purposes-and-scopes),
   provides context for ventilation standards. V2 makes no compliance claim.
6. ASHRAE, [Position Document on Indoor Carbon Dioxide](https://www.ashrae.org/file%20library/about/position%20documents/pd_indoorcarbondioxide_2022.pdf),
   provides context for interpreting indoor CO₂ and why it is not a complete
   indoor-air-quality metric.
