# Weather data

The repository does not redistribute third-party weather files by default.

For the Tabriz case, place the EnergyPlus EPW file here:

`IRN_Tabriz.407060_ITMY.epw`

Then run:

```bash
python scripts/run_epw_case.py \
  --epw data/observed/IRN_Tabriz.407060_ITMY.epw \
  --output outputs/tabriz_itmy
```

See `docs/DATA_PROVENANCE_TABRIZ.md` for source metadata and claim boundaries.
