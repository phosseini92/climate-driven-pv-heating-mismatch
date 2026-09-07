# Baseline results — synthetic benchmark

These results are generated from the deterministic synthetic cold-temperate benchmark and the illustrative baseline configuration:

- PV area: 30 m²
- PV efficiency: 18%
- heating base temperature: 18 °C
- building HLC: 120 W/K
- heat-pump COP: 3.0
- hourly timestep

## Results

- Annual PV generation: **8598.7 kWh_el**
- Annual useful heating demand: **9867.8 kWh_th**
- Annual heating electricity: **3289.3 kWh_el**
- Direct concurrent PV coverage of heating electricity: **32.6%**
- Annual deficit energy: **2217.1 kWh_el**
- Annual surplus energy: **7526.6 kWh_el**
- Deficit-hour fraction: **51.7%**
- Symmetric mismatch index: **0.820**

## Interpretation

The benchmark intentionally produces a heating-dominated winter and solar-dominated summer. Under the stated assumptions, annual PV generation exceeds annual heating electricity in aggregate, yet the direct concurrent PV coverage is only about **32.6%** and the symmetric mismatch index is **0.820**.

This demonstrates the distinction between **annual energy adequacy** and **temporal adequacy**. The result is a property of the synthetic benchmark and illustrative parameters; it is not evidence of performance for a real any real location building.

## Verification status

- 15 automated tests passed.
- Repeated synthetic runs produced byte-identical tracked CSV/JSON outputs.
- Empirical building or heat-pump validation has not been performed.

See `VALIDATION.md`, `LIMITATIONS.md`, and `RESEARCH_CLAIMS.md`.
