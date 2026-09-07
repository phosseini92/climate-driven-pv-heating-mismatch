# Methods

## 1. Weather input

The workflow accepts hourly:

- 2 m outdoor air temperature [°C]
- shortwave solar radiation / GHI [W/m²]

Two modes are supported:

1. a deterministic synthetic cold-temperate benchmark;
2. an optional observed/reanalysis weather CSV.

## 2. PV electricity

For each timestep:

`E_PV = GHI × A_PV × η_PV × Δt / 1000`

where:

- `GHI` is W/m²;
- `A_PV` is m²;
- `η_PV` is module/system screening efficiency;
- `Δt` is hours;
- `E_PV` is kWh_el.

This is a simplified screening model. It does not include tilt transposition, temperature coefficients, inverter efficiency, shading, soiling or degradation.

## 3. Space-heating proxy

The useful heating-energy proxy is:

`Q_heat = HLC × max(T_base − T_out, 0) × Δt / 1000`

where:

- `HLC` is a configurable lumped building heat-loss coefficient [W/K];
- `T_base` is the heating base temperature [°C];
- `Q_heat` is kWh_th.

This creates unit-consistent thermal energy but remains a steady-state proxy rather than a calibrated building model.

## 4. Electrification / heat-pump screening

Heating electricity is:

`E_heat = Q_heat / COP`

A constant COP is used only to screen the effect of heating electrification efficiency. It is not a dynamic heat-pump model.

## 5. Mismatch

Hourly balance:

`B(t) = E_PV(t) − E_heat(t)`

Positive values indicate concurrent surplus; negative values indicate deficit.

Primary mismatch index:

`SMI = Σ|E_PV − E_heat| / Σ(E_PV + E_heat)`

Direct concurrent PV coverage:

`Coverage = Σ min(E_PV, E_heat) / Σ E_heat`

No storage or grid exchange is assumed in these direct-match metrics.

## 6. Sensitivity

The default grid varies:

- `T_base`: 18, 20 °C
- `HLC`: 80, 120, 160 W/K
- `COP`: 2.5, 3.0, 4.0
- `PV area`: 20, 30, 40 m²

The values are illustrative scenario parameters, not archetype calibrations.
