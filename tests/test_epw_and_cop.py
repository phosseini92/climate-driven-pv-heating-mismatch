from pathlib import Path
import tempfile
import numpy as np
from climate_pv_heating.io import read_epw
from climate_pv_heating.heat_pump import linear_temperature_cop

HEADER = "\n".join([
    "LOCATION,Test,Test,IRN,TMY,000000,38.0,46.0,3.5,1000",
    "DESIGN CONDITIONS,0",
    "TYPICAL/EXTREME PERIODS,0",
    "GROUND TEMPERATURES,0",
    "HOLIDAYS/DAYLIGHT SAVINGS,No,0,0,0",
    "COMMENTS 1,fixture",
    "COMMENTS 2,fixture",
    "DATA PERIODS,1,1,Data,Sunday,1/ 1,12/31",
])

def row(year, month, day, hour, drybulb, ghi):
    vals = [
        year, month, day, hour, 60, "?9?9?9?9?9?9?9?9?9",
        drybulb, -5, 50, 90000,
        0, 0, 250, ghi, 0, 0,
        0, 0, 0, 0, 180, 2,
        5, 5, 20, 77777, 9, 999999999,
        10, 0.1, 0, 99, 0.2, 0, 1
    ]
    return ",".join(map(str, vals))

def test_epw_parser_extracts_temperature_and_ghi(tmp_path):
    p = tmp_path / "test.epw"
    p.write_text(HEADER + "\n" + row(2001,1,1,1,-5,0) + "\n" + row(2001,1,1,2,-4,10) + "\n")
    df, header = read_epw(p)
    assert len(df) == 2
    assert np.isclose(df.loc[0, "temperature_2m_c"], -5)
    assert np.isclose(df.loc[1, "shortwave_radiation_w_m2"], 10)
    assert df.loc[0, "time"].hour == 0
    assert len(header) == 8

def test_dynamic_cop_increases_with_outdoor_temperature():
    cop = linear_temperature_cop([-10, 0, 10])
    assert cop[0] < cop[1] < cop[2]

def test_dynamic_cop_is_bounded():
    cop = linear_temperature_cop([-100, 100])
    assert cop[0] >= 1.8
    assert cop[1] <= 4.5
