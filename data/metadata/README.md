# Weather-source metadata

The original EnergyPlus Tabriz ITMY `.epw`, `.ddy`, and `.stat` source files are not redistributed in this public repository.

Their filenames, provenance, station metadata, and SHA-256 hashes are documented in:

- `docs/DATA_PROVENANCE_TABRIZ.md`
- `case_studies/tabriz_iran_itmy.json`

The generated research outputs derived from the EPW run are retained in `outputs/tabriz_itmy/`.

To reproduce the case, obtain the Tabriz ITMY EnergyPlus weather package from the official EnergyPlus weather-data source and place:

`IRN_Tabriz.407060_ITMY.epw`

in `data/observed/`, then run the documented pipeline.
