from math import isclose

import pytest

from meter_calculations import (
    MeterInputs,
    calculate_discharge,
    discharge_at_deflection,
    recommended_cd,
)


def sample_input(**changes):
    values = {
        "meter_type": "Venturimeter",
        "inlet_diameter_mm": 100.0,
        "throat_diameter_mm": 50.0,
        "manometer_deflection_mm": 200.0,
        "fluid_density_kg_m3": 1000.0,
        "manometer_density_kg_m3": 13600.0,
        "coefficient_of_discharge": 0.98,
    }
    values.update(changes)
    return MeterInputs(**values)


def test_textbook_case_matches_manual_calculation():
    result = calculate_discharge(sample_input())

    assert isclose(result["pressure_difference_kpa"], 24.7212, rel_tol=1e-9)
    assert isclose(result["differential_head_m"], 2.52, rel_tol=1e-9)
    assert isclose(result["theoretical_discharge_l_s"], 14.259163, rel_tol=1e-6)
    assert isclose(result["actual_discharge_l_s"], 13.973979, rel_tol=1e-6)


def test_actual_discharge_is_cd_times_theoretical_discharge():
    result = calculate_discharge(sample_input(coefficient_of_discharge=0.62))
    ratio = result["actual_discharge_l_s"] / result["theoretical_discharge_l_s"]
    assert isclose(ratio, 0.62, rel_tol=1e-12)


def test_discharge_obeys_square_root_of_deflection():
    data = sample_input()
    q_200 = discharge_at_deflection(data, 200.0)
    q_800 = discharge_at_deflection(data, 800.0)
    assert isclose(q_800 / q_200, 2.0, rel_tol=1e-12)


def test_zero_deflection_gives_zero_discharge_and_velocity():
    result = calculate_discharge(sample_input(manometer_deflection_mm=0.0))
    assert result["actual_discharge_l_s"] == 0.0
    assert result["inlet_velocity_m_s"] == 0.0
    assert result["throat_velocity_m_s"] == 0.0


@pytest.mark.parametrize(
    "changes, message",
    [
        ({"throat_diameter_mm": 100.0}, "smaller than inlet"),
        ({"manometer_density_kg_m3": 900.0}, "must be denser"),
        ({"coefficient_of_discharge": 1.1}, "between 0 and 1"),
        ({"manometer_deflection_mm": -1.0}, "cannot be negative"),
    ],
)
def test_invalid_inputs_raise_clear_error(changes, message):
    with pytest.raises(ValueError, match=message):
        calculate_discharge(sample_input(**changes))


def test_representative_coefficients():
    assert recommended_cd("Venturimeter") == 0.98
    assert recommended_cd("Orifice meter") == 0.62
