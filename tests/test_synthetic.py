from climate_pv_heating.synthetic import generate_synthetic_hourly_year

def test_synthetic_non_leap_year_has_8760_hours():
    df = generate_synthetic_hourly_year(2023)
    assert len(df) == 8760

def test_synthetic_is_deterministic():
    a = generate_synthetic_hourly_year(2023)
    b = generate_synthetic_hourly_year(2023)
    assert a.equals(b)

def test_synthetic_has_winter_summer_contrast():
    df = generate_synthetic_hourly_year(2023)
    jan = df[df["time"].dt.month == 1]["temperature_2m_c"].mean()
    jul = df[df["time"].dt.month == 7]["temperature_2m_c"].mean()
    assert jul > jan
