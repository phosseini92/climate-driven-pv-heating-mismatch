import numpy as np
from climate_pv_heating.metrics import symmetric_mismatch_index

def test_mismatch_zero_for_identical_series():
    x = np.array([0, 1, 2, 3], dtype=float)
    assert np.isclose(symmetric_mismatch_index(x, x), 0.0)

def test_mismatch_one_for_disjoint_series():
    pv = np.array([1, 0], dtype=float)
    heat = np.array([0, 1], dtype=float)
    assert np.isclose(symmetric_mismatch_index(pv, heat), 1.0)

def test_mismatch_safe_for_all_zero():
    assert symmetric_mismatch_index([0, 0], [0, 0]) == 0.0
