# Case study — Tabriz ITMY

## Purpose

The Tabriz case tests whether the temporal PV–heating mismatch identified in the transparent synthetic benchmark persists when the same workflow is driven by an established building-energy weather file.

## Why Tabriz

Tabriz provides an independent cold-climate application consistent with the project's original heating-focused scope. It was not selected because of any particular doctoral vacancy or institution.

## Analysis sequence

1. parse EnergyPlus EPW dry-bulb temperature and global horizontal radiation;
2. run the same baseline HLC/PV/COP assumptions used in the synthetic benchmark;
3. compare annual and monthly energy balance;
4. compare direct concurrent PV coverage, deficit-hour fraction and symmetric mismatch index;
5. run the full HLC/COP/PV-area/base-temperature sensitivity grid;
6. test whether relaxing the constant-COP assumption materially changes mismatch conclusions.

## Status

The code path, parser, tests and comparison scripts are complete.

The case should be marked **executed** only after the source EPW file is present in `data/observed/` and the Tabriz output folder has been generated.
