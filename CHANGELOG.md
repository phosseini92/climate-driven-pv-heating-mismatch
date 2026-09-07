# Changelog

## v1.2.0

- Replaced the unexecuted 2023 reanalysis case concept with a documented EnergyPlus Tabriz ITMY case.
- Added EPW parser for dry-bulb temperature and global horizontal radiation.
- Added Tabriz case provenance and explicit typical-year claim boundaries.
- Executed the Tabriz ITMY case and documented results.
- Added 54-scenario Tabriz sensitivity grid and dynamic-COP sensitivity outputs.
- Added Synthetic vs Tabriz quantitative comparison.
- Added EPW-specific repeated-run reproducibility verification.
- Added Synthetic vs Tabriz comparison pipeline.
- Added optional outdoor-temperature-dependent COP sensitivity model.
- Added automated tests for EPW parsing and dynamic COP bounds.
- Kept the core model fully location-agnostic.
- Explicitly distinguished typical-weather testing from field validation.

## v1.1.0

- Removed location-specific defaults from the core workflow.
- Reframed the repository as explicitly location-agnostic.
- Added an independent cold-climate case configuration pathway.
- Clarified project chronology: conceptual cold-climate analysis first; reproducible extension later.

## v1.0.0

- Reframed the preliminary normalized mismatch analysis as a unit-consistent hourly screening workflow.
- Added lumped HLC-based useful heating-energy proxy.
- Added constant-COP heating electrification screening.
- Added symmetric mismatch index and direct concurrent PV coverage.
- Added 54-scenario default sensitivity grid.
- Added deterministic synthetic hourly benchmark.
- Added automated tests, explicit claim boundaries, assumptions, limitations and reproducibility audit.
