# Synthetic benchmark vs Tabriz ITMY

## Purpose

The synthetic benchmark exists for analytical transparency. The Tabriz ITMY case tests whether the same qualitative PV–heating mismatch persists under an established building-energy typical-year weather file.

## Key comparison

| Metric | Synthetic benchmark | Tabriz ITMY |
|---|---:|---:|
| Annual PV generation [kWh_el] | 8598.7 | 7466.1 |
| Annual useful heating demand [kWh_th] | 9867.8 | 8620.2 |
| Heating electricity, COP 3 [kWh_el] | 3289.3 | 2873.4 |
| Direct concurrent PV coverage | 32.6% | 33.3% |
| Deficit-hour fraction | 51.7% | 42.3% |
| Symmetric mismatch index | 0.820 | 0.815 |

## Interpretation

The absolute annual energies differ between the two weather inputs, but the temporal-mismatch conclusion is stable:

- direct concurrent PV coverage remains close to one-third in both cases;
- the symmetric mismatch index remains high in both cases (**0.820** synthetic vs **0.815** Tabriz ITMY);
- substantial annual PV production therefore does not remove the need to consider temporal flexibility, storage, demand management, grid interaction or more detailed thermal-system modelling.

This is a transferability check of the **screening logic**, not validation of a real building.
