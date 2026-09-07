from dataclasses import dataclass

@dataclass(frozen=True)
class ModelConfig:
    """Illustrative screening parameters; not calibrated to a specific building."""
    pv_area_m2: float = 30.0
    pv_efficiency: float = 0.18
    heating_base_temp_c: float = 18.0
    heat_loss_coefficient_w_per_k: float = 120.0
    heat_pump_cop: float = 3.0
    timestep_hours: float = 1.0

    def validate(self) -> None:
        if self.pv_area_m2 <= 0:
            raise ValueError("pv_area_m2 must be > 0")
        if not (0 < self.pv_efficiency <= 1):
            raise ValueError("pv_efficiency must be in (0, 1]")
        if self.heat_loss_coefficient_w_per_k <= 0:
            raise ValueError("heat_loss_coefficient_w_per_k must be > 0")
        if self.heat_pump_cop <= 0:
            raise ValueError("heat_pump_cop must be > 0")
        if self.timestep_hours <= 0:
            raise ValueError("timestep_hours must be > 0")
