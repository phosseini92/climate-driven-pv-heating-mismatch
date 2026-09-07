# Results — Tabriz ITMY case

## Weather-file QA

The EnergyPlus EPW contains:

- 8,760 hourly records
- no duplicated timestamps after interval-start remapping
- no missing required dry-bulb temperature or global-horizontal-radiation values
- dry-bulb temperature range: **−15.0 to 37.0 °C**
- global horizontal radiation range: **0 to 764 Wh/m² per hourly interval**
- station elevation: **1,361 m**

The accompanying `.stat` file reports approximately **2,921 annual heating degree-days at an 18 °C baseline** for the weather file, supporting the interpretation of Tabriz as a heating-relevant climate case.

## Baseline model assumptions

The same illustrative baseline used for the synthetic benchmark is retained:

- PV area: 30 m²
- PV efficiency: 18%
- heating base temperature: 18 °C
- building heat-loss coefficient: 120 W/K
- constant heat-pump COP: 3.0
- hourly timestep

The model is not calibrated to a specific Tabriz building.

## Baseline results

- Annual PV generation: **7466.1 kWh_el**
- Annual useful heating demand proxy: **8620.2 kWh_th**
- Annual heating electricity at COP 3: **2873.4 kWh_el**
- Direct concurrent PV coverage of heating electricity: **33.3%**
- Annual deficit energy: **1915.4 kWh_el**
- Annual surplus energy: **6508.1 kWh_el**
- Deficit-hour fraction: **42.3%**
- Symmetric mismatch index: **0.815**

## Monthly pattern

The Tabriz ITMY case shows net monthly electricity deficits in **January, February, and December**, while March through November are net-positive under the illustrative PV and heating assumptions.

This annual surplus does not imply temporal adequacy. Only about **33.3%** of annual heating electricity is met by concurrent PV generation without storage or grid exchange.

## Parameter sensitivity

The 54-scenario grid spans:

- HLC: 80–160 W/K
- COP: 2.5–4.0
- PV area: 20–40 m²
- heating base temperature: 18–20 °C

Across this grid:

- direct PV coverage ranges from **25.6% to 37.3%**
- symmetric mismatch index ranges from **0.734 to 0.907**
- annual heating electricity ranges from **1436.7 to 5368.7 kWh**

The spread confirms that mismatch conclusions depend materially on building heat loss, electrification efficiency and PV sizing.

## Dynamic COP screening

Relaxing the constant-COP assumption increases annual heating electricity in the illustrative temperature-dependent COP scenarios:

- constant COP 3: **2873.4 kWh_el**
- linear mild: **3150.7 kWh_el**
- linear baseline: **3338.9 kWh_el**
- linear steeper: **3521.7 kWh_el**

These are sensitivity cases, not a manufacturer-calibrated heat-pump model.

## QA status

- all energy-accounting identities close to floating-point precision
- 18/18 automated tests pass
- synthetic tracked outputs are byte-identical across repeated runs
- Tabriz EPW-driven tracked outputs are byte-identical across repeated runs

## Claim boundary

This is a **verified and sensitivity-tested typical-weather screening case**. It is not field validation, calibrated building simulation, or detailed HVAC/heat-pump modelling.
