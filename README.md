# Climate-Driven PV–Heating Demand Mismatch

**A reproducible weather-to-energy screening workflow for seasonal heating-electrification mismatch**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#)
[![Status](https://img.shields.io/badge/status-v1.2%20screening%20workflow-green)](#)
[![Tests](https://img.shields.io/badge/tests-pytest-informational)](#)

## Project origin

This project began as a preliminary conceptual analysis of seasonal mismatch between photovoltaic (PV) generation and temperature-driven heating demand in a generic cold-climate context. The original analysis used synthetic daily temperature and solar-radiation profiles to make the seasonal relationship transparent.

The current repository develops that earlier work into a **reproducible, unit-consistent, sensitivity-tested screening workflow**. The core model remains location-agnostic. A separate Tabriz, Iran ITMY case is included as an independent typical-weather application.

## Research question

> How strongly does the temporal alignment between PV generation and electrified space-heating demand depend on weather, building heat-loss assumptions, heat-pump COP, and PV sizing?

## What changed from the preliminary analysis

The original conceptual analysis compared normalized PV generation with a temperature-based heating-demand proxy. Version 1.2 improves that structure by:

1. working at **hourly** resolution;
2. converting temperature deficit into an illustrative **thermal heating-energy demand** using a configurable building heat-loss coefficient (HLC);
3. converting thermal demand into **electricity demand** using a configurable heat-pump coefficient of performance (COP);
4. comparing PV electricity and heating electricity in consistent **kWh** units;
5. reporting interpretable mismatch metrics rather than relying only on curve normalization;
6. adding systematic sensitivity analysis;
7. adding automated tests, explicit assumptions, claim boundaries and reproducibility checks;
8. supporting separately configured typical-weather EPW cases without embedding a location into the core model itself.

## Core outputs

The baseline pipeline reports:

- annual PV generation [kWh]
- annual useful heating demand [kWh_th]
- annual heat-pump electricity demand [kWh_el]
- direct concurrent PV coverage of heating electricity demand
- annual deficit energy [kWh]
- annual surplus energy [kWh]
- deficit-hour fraction
- symmetric mismatch index
- monthly energy-balance summaries

The sensitivity workflow varies:

- heating base temperature
- building heat-loss coefficient (HLC)
- heat-pump COP
- PV area

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/run_baseline.py
python scripts/run_sensitivity.py
pytest -q
```

Outputs are written to `outputs/`.

## Typical-weather case study

The core model is location-agnostic. A separate **Tabriz, Iran ITMY** case is configured for building-energy screening using an EnergyPlus EPW file.

Case metadata:

- station: `407060`
- weather type: `ITMY`
- case file: `case_studies/tabriz_iran_itmy.json`
- expected EPW: `data/observed/IRN_Tabriz.407060_ITMY.epw`

Run:

```bash
python scripts/run_epw_case.py \
  --epw data/observed/IRN_Tabriz.407060_ITMY.epw \
  --output outputs/tabriz_itmy

python scripts/compare_synthetic_tabriz.py
python scripts/run_dynamic_cop_sensitivity.py \
  --epw data/observed/IRN_Tabriz.407060_ITMY.epw
```

The Tabriz ITMY case has now been executed and QA-checked. It is a **typical meteorological year**, not an actual calendar-year dataset and not field validation. See `docs/DATA_PROVENANCE_TABRIZ.md`, `docs/RESULTS_TABRIZ_ITMY.md`, and `docs/COMPARISON_SYNTHETIC_TABRIZ.md`.

## Executed Tabriz ITMY result snapshot

Under the illustrative baseline assumptions:

- PV generation: **7466.1 kWh_el**
- heating electricity at COP 3: **2873.4 kWh_el**
- direct concurrent PV coverage: **33.3%**
- symmetric mismatch index: **0.815**

The synthetic benchmark and Tabriz ITMY case therefore lead to the same qualitative conclusion: annual PV adequacy does not imply temporal adequacy for electrified space heating.

See `docs/RESULTS_TABRIZ_ITMY.md`.

## Interpretation

A positive hourly balance means PV generation exceeds heating electricity demand in that hour. A negative balance means heating electricity demand exceeds concurrent PV generation.

The primary mismatch metric is:

`SMI = Σ|PV - Heating_el| / Σ(PV + Heating_el)`

where `0` indicates perfect temporal matching and values approaching `1` indicate increasing temporal separation.

The direct concurrent PV coverage ratio is:

`Σ min(PV, Heating_el) / Σ Heating_el`

This is a screening metric and does **not** include storage, grid exchange, curtailment, dynamic heat-pump performance or building thermal mass.

## Scientific boundaries

### Supported

- reproducible comparison of PV electricity and temperature-driven heating-electricity demand under stated assumptions;
- sensitivity of temporal mismatch to HLC, COP, PV area and base temperature;
- comparison of a transparent synthetic benchmark with separately configured typical-weather cases;
- identification of periods where more detailed storage, flexibility or building simulation may be warranted.

### Not supported

- calibrated prediction of a real building's heating load;
- detailed heat-pump performance or control;
- HVAC simulation;
- grid-impact assessment;
- optimal PV or storage sizing;
- district-heating simulation;
- claims of field validation.

See `docs/RESEARCH_CLAIMS.md` and `docs/LIMITATIONS.md`.

## Repository structure

```text
case_studies/
    tabriz_iran_itmy.json
data/
    metadata/
    observed/
docs/
outputs/
    baseline/
    comparison/
    sensitivity/
    tabriz_itmy/
scripts/
    compare_synthetic_tabriz.py
    reproducibility_check.py
    reproducibility_check_epw.py
    run_baseline.py
    run_dynamic_cop_sensitivity.py
    run_epw_case.py
    run_sensitivity.py
src/
    climate_pv_heating/
        __init__.py
        config.py
        heat_pump.py
        io.py
        metrics.py
        models.py
        pipeline.py
        plots.py
        sensitivity.py
        synthetic.py
tests/
CHANGELOG.md
CITATION.cff
LICENSE
README.md
SOURCE_MANIFEST.sha256
pyproject.toml
requirements.txt
```

## Data provenance

Synthetic inputs are generated internally by `src/climate_pv_heating/synthetic.py`.

The executed Tabriz case uses the EnergyPlus `IRN_Tabriz.407060_ITMY` typical meteorological year (ITMY) weather file. Third-party `.epw`, `.ddy`, and `.stat` source files are **not redistributed** in this public repository. Their station metadata, source information, and SHA-256 hashes are documented in `docs/DATA_PROVENANCE_TABRIZ.md` and `case_studies/tabriz_iran_itmy.json`.

Generated Tabriz outputs are retained in `outputs/tabriz_itmy/`. To reproduce the case, obtain the official Tabriz ITMY EPW file, place it at `data/observed/IRN_Tabriz.407060_ITMY.epw`, and run the documented EPW workflow.

## Citation

See `CITATION.cff`.

## Licence

MIT. See `LICENSE`.
