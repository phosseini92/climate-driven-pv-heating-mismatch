# Limitations

1. **Lumped heating proxy**  
   Building heat loss is represented through a single HLC. Thermal mass, ventilation dynamics, internal gains, solar gains, infiltration, occupancy and controls are omitted.

2. **Constant heat-pump COP**  
   COP is not a function of outdoor temperature, flow temperature, part load, defrost or control.

3. **Simplified PV conversion**  
   GHI is converted directly using area and efficiency. Tilt, azimuth, temperature effects, inverter losses, shading, soiling and degradation are omitted.

4. **No storage or network model**  
   Deficit and surplus are screening metrics. No battery, thermal store, grid export/import, curtailment or demand response is dispatched.

5. **Synthetic benchmark is conceptual**  
   The synthetic climate is deterministic and not a meteorological representation of a real-weather case or any other location.

6. **Observed-data mode is weather-driven, not field validation**  
   Reanalysis weather improves climatic realism but does not calibrate the building or heating system.

7. **No optimisation**  
   The repository does not select optimal PV size, HLC, COP or storage capacity.

These limitations are deliberate: the workflow is intended to expose temporal mismatch and test parameter sensitivity before more detailed building-energy, heat-pump, storage or grid modelling.
