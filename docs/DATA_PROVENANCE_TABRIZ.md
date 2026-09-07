# Tabriz weather-data provenance

## Case

- Location: Tabriz, Iran
- EnergyPlus station: 407060
- Weather type: ITMY — Iranian Typical Meteorological Year
- File format: EnergyPlus Weather (EPW)
- Expected file name: `IRN_Tabriz.407060_ITMY.epw`
- EnergyPlus listing coordinates: approximately 38.05° N, 46.17° E

## Why ITMY is used

The Tabriz case is intended as a **typical-weather building-energy screening case**, not as an actual-year meteorological reconstruction. This distinction is important.

The repository therefore uses the labels:

- `Tabriz ITMY case`
- `typical meteorological weather`
- `EnergyPlus EPW`

and does **not** use:

- `Tabriz 2023 actual weather`
- `field-measured Tabriz weather`
- `observed 2023 building data`

## Source file

Primary EnergyPlus endpoint:

`https://energyplus.net/weather-download/asia_wmo_region_2/IRN//IRN_Tabriz.407060_ITMY/IRN_Tabriz.407060_ITMY.epw`

Mirror/listing:

`https://energyplus-weather.s3.amazonaws.com/asia_wmo_region_2/IRN/IRN_Tabriz.407060_ITMY/IRN_Tabriz.407060_ITMY.zip`

## Claim boundary

An ITMY file improves climatic realism relative to the repository's synthetic benchmark, but it does not validate the building heat-loss coefficient, the heat-pump COP model, PV-system assumptions, or actual energy use.

The case is therefore a **typical-weather sensitivity and transferability test**, not field validation.

## Local source-file verification

- `IRN_Tabriz.407060_ITMY.epw` SHA-256: `0f8cc6cb3d63a951d56a9a2dc94e9f635b97eab70909086c4335a0b25c875fba`
- `IRN_Tabriz.407060_ITMY.ddy` SHA-256: `51d0b43848f2286b4777c86a09dbc8a8715226ef6e9ff43cb3815d7dc239dae6`
- `IRN_Tabriz.407060_ITMY.stat` SHA-256: `6a1193cddd6f92b6aba00782f9fc909e94a00f594f65717d469ba2b5852de2f7`

The EPW case was executed successfully and produced 8,760 hourly model records.
