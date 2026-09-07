import numpy as np

def linear_temperature_cop(
    temperature_c,
    cop_at_reference=3.0,
    reference_temperature_c=7.0,
    slope_per_k=0.06,
    min_cop=1.8,
    max_cop=4.5,
):
    """
    Illustrative outdoor-temperature-dependent COP sensitivity curve.

    COP = clip(COP_ref + slope * (T_out - T_ref), min_cop, max_cop)

    This is not a manufacturer or system performance map. It exists only to test
    whether conclusions are sensitive to relaxing the constant-COP assumption.
    """
    t = np.asarray(temperature_c, dtype=float)
    cop = cop_at_reference + slope_per_k * (t - reference_temperature_c)
    return np.clip(cop, min_cop, max_cop)

def dynamic_heating_electricity_kwh(useful_heating_kwh_th, temperature_c, **cop_kwargs):
    q = np.asarray(useful_heating_kwh_th, dtype=float)
    cop = linear_temperature_cop(temperature_c, **cop_kwargs)
    return q / cop, cop
