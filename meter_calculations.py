"""Engineering calculations for differential-pressure flow meters.

The equations in this module assume steady, incompressible flow through a
horizontal pipe and a heavier manometric liquid in a differential U-tube.
Keeping the calculations separate from Streamlit makes them easy to test and
explain during a viva.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sqrt


GRAVITY_M_S2 = 9.81
STANDARD_CD = {
    "Venturimeter": 0.98,
    "Orifice meter": 0.62,
}


@dataclass(frozen=True)
class MeterInputs:
    """Input values for a Venturimeter or Orifice meter calculation."""

    meter_type: str
    inlet_diameter_mm: float
    throat_diameter_mm: float
    manometer_deflection_mm: float
    fluid_density_kg_m3: float
    manometer_density_kg_m3: float
    coefficient_of_discharge: float
    gravity_m_s2: float = GRAVITY_M_S2


def validate_inputs(data: MeterInputs) -> None:
    """Raise ``ValueError`` when an input cannot represent this model."""

    if data.meter_type not in STANDARD_CD:
        raise ValueError("Select either Venturimeter or Orifice meter.")
    if data.inlet_diameter_mm <= 0:
        raise ValueError("Inlet diameter must be greater than zero.")
    if data.throat_diameter_mm <= 0:
        raise ValueError("Throat/orifice diameter must be greater than zero.")
    if data.throat_diameter_mm >= data.inlet_diameter_mm:
        raise ValueError("Throat/orifice diameter must be smaller than inlet diameter.")
    if data.manometer_deflection_mm < 0:
        raise ValueError("Manometer deflection cannot be negative.")
    if data.fluid_density_kg_m3 <= 0 or data.manometer_density_kg_m3 <= 0:
        raise ValueError("Both fluid densities must be greater than zero.")
    if data.manometer_density_kg_m3 <= data.fluid_density_kg_m3:
        raise ValueError(
            "Manometer liquid must be denser than the flowing liquid for this setup."
        )
    if not 0 < data.coefficient_of_discharge <= 1:
        raise ValueError("Coefficient of discharge must be between 0 and 1.")
    if data.gravity_m_s2 <= 0:
        raise ValueError("Gravitational acceleration must be greater than zero.")


def calculate_discharge(data: MeterInputs) -> dict[str, float | str]:
    """Calculate pressure difference, theoretical discharge and actual discharge.

    Returns SI values plus convenient litre-per-second values used by the UI.
    """

    validate_inputs(data)

    diameter_1_m = data.inlet_diameter_mm / 1000.0
    diameter_2_m = data.throat_diameter_mm / 1000.0
    deflection_m = data.manometer_deflection_mm / 1000.0

    area_1_m2 = pi * diameter_1_m**2 / 4.0
    area_2_m2 = pi * diameter_2_m**2 / 4.0
    beta = diameter_2_m / diameter_1_m

    pressure_difference_pa = (
        data.manometer_density_kg_m3 - data.fluid_density_kg_m3
    ) * data.gravity_m_s2 * deflection_m
    differential_head_m = pressure_difference_pa / (
        data.fluid_density_kg_m3 * data.gravity_m_s2
    )

    geometry_factor = area_2_m2 / sqrt(1.0 - beta**4)
    theoretical_discharge_m3_s = geometry_factor * sqrt(
        2.0 * pressure_difference_pa / data.fluid_density_kg_m3
    )
    actual_discharge_m3_s = (
        data.coefficient_of_discharge * theoretical_discharge_m3_s
    )

    inlet_velocity_m_s = actual_discharge_m3_s / area_1_m2
    throat_velocity_m_s = actual_discharge_m3_s / area_2_m2
    discharge_reduction_percent = (1.0 - data.coefficient_of_discharge) * 100.0

    return {
        "meter_type": data.meter_type,
        "diameter_1_m": diameter_1_m,
        "diameter_2_m": diameter_2_m,
        "area_1_m2": area_1_m2,
        "area_2_m2": area_2_m2,
        "beta": beta,
        "deflection_m": deflection_m,
        "pressure_difference_pa": pressure_difference_pa,
        "pressure_difference_kpa": pressure_difference_pa / 1000.0,
        "differential_head_m": differential_head_m,
        "theoretical_discharge_m3_s": theoretical_discharge_m3_s,
        "theoretical_discharge_l_s": theoretical_discharge_m3_s * 1000.0,
        "actual_discharge_m3_s": actual_discharge_m3_s,
        "actual_discharge_l_s": actual_discharge_m3_s * 1000.0,
        "actual_discharge_l_min": actual_discharge_m3_s * 60_000.0,
        "inlet_velocity_m_s": inlet_velocity_m_s,
        "throat_velocity_m_s": throat_velocity_m_s,
        "discharge_reduction_percent": discharge_reduction_percent,
    }


def discharge_at_deflection(
    data: MeterInputs,
    deflection_mm: float,
    coefficient_of_discharge: float | None = None,
) -> float:
    """Return actual discharge in L/s at another manometer deflection."""

    adjusted = MeterInputs(
        meter_type=data.meter_type,
        inlet_diameter_mm=data.inlet_diameter_mm,
        throat_diameter_mm=data.throat_diameter_mm,
        manometer_deflection_mm=deflection_mm,
        fluid_density_kg_m3=data.fluid_density_kg_m3,
        manometer_density_kg_m3=data.manometer_density_kg_m3,
        coefficient_of_discharge=(
            data.coefficient_of_discharge
            if coefficient_of_discharge is None
            else coefficient_of_discharge
        ),
        gravity_m_s2=data.gravity_m_s2,
    )
    return float(calculate_discharge(adjusted)["actual_discharge_l_s"])


def recommended_cd(meter_type: str) -> float:
    """Return a representative coefficient used for classroom comparison."""

    try:
        return STANDARD_CD[meter_type]
    except KeyError as exc:
        raise ValueError("Unknown meter type.") from exc
