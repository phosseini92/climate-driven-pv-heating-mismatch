# Verification and validation status

## What is verified

The repository uses automated tests to verify:

- PV unit conversion;
- zero PV generation at zero radiation;
- zero heating demand above the base temperature;
- heating-energy unit conversion;
- monotonic response to HLC;
- monotonic response to COP;
- monotonic response to PV area;
- mismatch-index limiting cases;
- deterministic synthetic weather generation;
- explicit observed-data API parameter construction.

A repeated-run reproducibility script compares SHA-256 hashes of tracked CSV/JSON outputs.

## What is not validated

The workflow is **not empirically calibrated or field validated** against:

- measured building heating demand;
- measured heat-pump electricity;
- indoor temperature;
- a specific building archetype;
- district-heating data;
- distribution-grid measurements.

Accordingly, this repository should be described as a:

**verified, sensitivity-tested climate–energy screening workflow**

and not as a validated building heating model.


## Tabriz ITMY execution

The Tabriz ITMY EPW was parsed successfully into 8,760 hourly records.

QA checks confirmed:

- no duplicate mapped timestamps;
- no missing required temperature or radiation values;
- no negative global-horizontal-radiation values;
- exact energy-accounting closure to floating-point precision;
- dimensionless metrics within valid bounds;
- byte-identical tracked outputs across two independent EPW-driven runs.

The Tabriz case remains typical-weather screening rather than field validation.
