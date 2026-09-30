"""FlowLab — Venturimeter and Orifice Meter Discharge Calculator."""

from __future__ import annotations

import csv
from io import StringIO

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

from meter_calculations import (
    MeterInputs,
    calculate_discharge,
    recommended_cd,
)


# Project members shown in the app footer.
PROJECT_MEMBERS = (
    ("GURMEET SINGH BANSAL", "25012250610059"),
)

FLOWING_FLUIDS = {
    "Water": 1000.0,
    "Kerosene": 820.0,
    "Light oil": 850.0,
    "Glycerin": 1260.0,
}
MANOMETER_FLUIDS = {
    "Mercury": 13600.0,
    "Carbon tetrachloride": 1600.0,
    "Dense salt solution": 1200.0,
}


st.set_page_config(
    page_title="FlowLab | Discharge Meter Calculator",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_styles() -> None:
    """Apply a modern dark-blue engineering dashboard theme."""

    st.markdown(
        """
        <style>
        :root {
            --ink: #e8eef7;
            --muted: #9fb0c4;
            --line: #2b3a4d;
            --panel: #172231;
            --panel-2: #1d2a3a;
            --navy: #0b1320;
            --blue: #4da3ff;
            --cyan: #35d0ba;
            --orange: #ff9f43;
            --wash: #0b1220;
        }

        .stApp {
            background:
                radial-gradient(circle at 80% 0%, rgba(53,208,186,.08), transparent 30%),
                radial-gradient(circle at 10% 20%, rgba(77,163,255,.07), transparent 28%),
                var(--wash);
            color: var(--ink);
        }

        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111c2b 0%, #0d1725 100%);
            border-right: 1px solid #263548;
        }
        [data-testid="stSidebar"] * { color: #e8eef7; }
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: #172231 !important;
        }
        [data-testid="stSidebar"] label p {
            font-weight: 650;
            letter-spacing: .01em;
        }

        [data-testid="stMetric"] {
            background: linear-gradient(145deg, #182638, #131f2d);
            border: 1px solid #2b3a4d;
            border-top: 3px solid var(--cyan);
            border-radius: 14px;
            padding: 16px 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,.18);
        }
        [data-testid="stMetricLabel"] { color: var(--muted); }
        [data-testid="stMetricValue"] { color: #f3f7fc; }

        .hero {
            background:
                radial-gradient(circle at 90% 15%, rgba(53,208,186,.20), transparent 25%),
                linear-gradient(135deg, #10233b 0%, #123b59 55%, #0b5b62 100%);
            color: white;
            border: 1px solid rgba(118,178,218,.18);
            border-radius: 18px;
            padding: 30px 32px;
            margin: 2px 0 18px;
            box-shadow: 0 16px 40px rgba(0,0,0,.22);
            position: relative;
            overflow: hidden;
        }
        .hero:after {
            content: "";
            position: absolute;
            width: 190px;
            height: 190px;
            border: 35px solid rgba(255,255,255,.06);
            border-radius: 50%;
            right: -45px;
            top: -82px;
        }
        .eyebrow {
            color: #65e3d2;
            font-weight: 800;
            font-size: .76rem;
            letter-spacing: .15em;
            text-transform: uppercase;
        }
        .hero h1 {
            margin: 8px 0 7px;
            font-size: clamp(2rem, 5vw, 3.25rem);
            color: #ffffff;
        }
        .hero p {
            color: #d6e6f4;
            margin: 0;
            max-width: 760px;
            line-height: 1.65;
        }

        .section-kicker {
            color: var(--cyan);
            font-size: .76rem;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
            margin-bottom: 4px;
        }

        .result-note {
            background: linear-gradient(90deg, rgba(53,208,186,.13), rgba(77,163,255,.07));
            border-left: 4px solid var(--cyan);
            border-top: 1px solid rgba(53,208,186,.18);
            border-right: 1px solid rgba(53,208,186,.10);
            border-bottom: 1px solid rgba(53,208,186,.10);
            color: #dcecf5;
            padding: 13px 16px;
            border-radius: 8px;
            margin: 10px 0 18px;
        }

        .formula-card, .info-card, .student-card {
            background: linear-gradient(145deg, #182638, #141f2d);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 18px 20px;
            margin: 8px 0 14px;
            box-shadow: 0 8px 25px rgba(0,0,0,.14);
        }
        .student-card { border-left: 4px solid var(--orange); }
        .small-note { color: var(--muted); font-size: .84rem; }

        div[data-baseweb="tab-list"] { gap: 10px; }
        button[data-baseweb="tab"] {
            background: #141f2d;
            color: #aebed0;
            border: 1px solid #2b3a4d;
            border-radius: 10px;
            padding: 10px 16px;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #183a55, #15545b);
            color: #ffffff;
            border-color: #3bbdac;
        }

        .stDownloadButton button {
            background: linear-gradient(135deg, #155b70, #147f79);
            color: white;
            border: 0;
            border-radius: 9px;
        }
        .stDownloadButton button:hover {
            background: linear-gradient(135deg, #1a6c82, #199087);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #2b3a4d;
            border-radius: 10px;
            overflow: hidden;
        }

        .stAlert {
            border-radius: 10px;
        }

        @media (max-width: 700px) {
            .hero { padding: 22px 20px; }
            .hero h1 { font-size: 2.15rem; }
            [data-testid="stMetric"] { padding: 13px 14px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def meter_animation(meter_type: str, result: dict[str, float | str]) -> str:
    """Return an animated SVG schematic for the selected meter."""

    flow_speed = max(0.9, min(3.2, 3.0 - float(result["actual_discharge_l_s"]) / 15.0))
    pressure_kpa = float(result["pressure_difference_kpa"])
    q_actual = float(result["actual_discharge_l_s"])

    if meter_type == "Venturimeter":
        pipe_shape = "M34 82 H190 L250 108 H370 L430 82 H666 V158 H430 L370 132 H250 L190 158 H34 Z"
        meter_feature = """
        <text x="310" y="49" text-anchor="middle" class="label">THROAT</text>
        <line x1="310" y1="56" x2="310" y2="102" class="guide"/>
        """
        device_name = "VENTURIMETER"
    else:
        pipe_shape = "M34 82 H666 V158 H34 Z"
        meter_feature = """
        <rect x="329" y="65" width="14" height="110" rx="2" fill="#f2a65a" stroke="#b45116" stroke-width="2"/>
        <circle cx="336" cy="120" r="25" fill="#d9f1f5" stroke="#b45116" stroke-width="2"/>
        <text x="336" y="48" text-anchor="middle" class="label">ORIFICE PLATE</text>
        <line x1="336" y1="55" x2="336" y2="88" class="guide"/>
        """
        device_name = "ORIFICE METER"

    particles = "".join(
        f'<circle class="particle p{i}" cx="{70 + i * 92}" cy="120" r="5"/>'
        for i in range(7)
    )

    return f"""
    <!doctype html>
    <html><head><meta charset="utf-8"><style>
    * {{ box-sizing: border-box; }}
    body {{ margin:0; background:#ffffff; font-family:Inter,system-ui,sans-serif; color:#102a43; }}
    .frame {{ border:1px solid #d9e2ec; border-radius:12px; padding:12px 14px 6px; overflow:hidden; }}
    .top {{ display:flex; justify-content:space-between; align-items:center; margin:0 7px 2px; }}
    .tag {{ font-size:12px; font-weight:800; letter-spacing:.12em; color:#008985; }}
    .live {{ font-size:12px; color:#627d98; }}
    .dot {{ display:inline-block; width:7px; height:7px; border-radius:50%; background:#20b486; margin-right:6px; animation:pulse 1.3s infinite; }}
    svg {{ width:100%; height:auto; display:block; }}
    .pipe {{ fill:url(#water); stroke:#315b72; stroke-width:4; }}
    .pipe-outline {{ fill:none; stroke:#173f5f; stroke-width:4; stroke-linejoin:round; }}
    .particle {{ fill:#ffffff; opacity:.85; animation:flow {flow_speed:.2f}s linear infinite; }}
    .p1 {{ animation-delay:-.3s }} .p2 {{ animation-delay:-.7s }} .p3 {{ animation-delay:-1.1s }}
    .p4 {{ animation-delay:-1.5s }} .p5 {{ animation-delay:-1.9s }} .p6 {{ animation-delay:-2.3s }}
    .tap {{ stroke:#315b72; stroke-width:4; fill:none; }}
    .manometer {{ stroke:#728a9c; stroke-width:14; stroke-linecap:round; fill:none; }}
    .mercury {{ stroke:#e8673c; stroke-width:9; stroke-linecap:round; fill:none; }}
    .label {{ font-size:12px; font-weight:800; fill:#526d82; letter-spacing:.08em; }}
    .reading {{ font-size:13px; font-weight:700; fill:#102a43; }}
    .guide {{ stroke:#90a4ae; stroke-width:1.5; stroke-dasharray:4 4; }}
    .arrow {{ fill:#ffffff; font-size:22px; font-weight:800; }}
    @keyframes flow {{ from {{ transform:translateX(-90px); }} to {{ transform:translateX(90px); }} }}
    @keyframes pulse {{ 50% {{ opacity:.35; transform:scale(.8); }} }}
    @media (prefers-reduced-motion:reduce) {{ .particle,.dot {{ animation:none; }} }}
    </style></head><body>
      <div class="frame">
        <div class="top"><span class="tag">{device_name} · LIVE SCHEMATIC</span><span class="live"><span class="dot"></span>{q_actual:.2f} L/s</span></div>
        <svg viewBox="0 0 700 355" role="img" aria-label="Animated {meter_type} with differential manometer">
          <defs>
            <linearGradient id="water" x1="0" x2="1"><stop offset="0" stop-color="#49bad1"/><stop offset="1" stop-color="#087f9c"/></linearGradient>
            <clipPath id="pipeClip"><path d="{pipe_shape}"/></clipPath>
          </defs>
          <path d="{pipe_shape}" class="pipe"/>
          <g clip-path="url(#pipeClip)">{particles}</g>
          <path d="{pipe_shape}" class="pipe-outline"/>
          {meter_feature}
          <text x="61" y="126" class="arrow">→</text>
          <text x="615" y="126" class="arrow">→</text>
          <line x1="205" y1="158" x2="205" y2="211" class="tap"/>
          <line x1="430" y1="158" x2="430" y2="211" class="tap"/>
          <path d="M205 211 V273 Q205 315 247 315 H388 Q430 315 430 273 V211" class="manometer"/>
          <path d="M205 259 V273 Q205 315 247 315 H388 Q430 315 430 273 V238" class="mercury"/>
          <line x1="455" y1="238" x2="455" y2="259" stroke="#ef7d32" stroke-width="2"/>
          <path d="M450 242 L455 235 L460 242 M450 255 L455 262 L460 255" fill="none" stroke="#ef7d32" stroke-width="2"/>
          <text x="470" y="254" class="reading">x = {float(result['deflection_m']) * 1000:.0f} mm</text>
          <text x="317" y="344" text-anchor="middle" class="reading">Δp = {pressure_kpa:.2f} kPa</text>
          <text x="170" y="185" class="label">P₁</text><text x="441" y="185" class="label">P₂</text>
        </svg>
      </div>
    </body></html>
    """


def create_comparison_figure(data: MeterInputs) -> plt.Figure:
    """Plot discharge against manometer deflection for both meter types."""

    maximum_x = max(400.0, data.manometer_deflection_mm * 1.65)
    deflections = np.linspace(0.0, maximum_x, 121)
    d1 = data.inlet_diameter_mm / 1000.0
    d2 = data.throat_diameter_mm / 1000.0
    a2 = np.pi * d2**2 / 4.0
    beta = d2 / d1
    delta_p = (
        (data.manometer_density_kg_m3 - data.fluid_density_kg_m3)
        * data.gravity_m_s2
        * deflections
        / 1000.0
    )
    q_theoretical_l_s = (
        a2
        / np.sqrt(1.0 - beta**4)
        * np.sqrt(2.0 * delta_p / data.fluid_density_kg_m3)
        * 1000.0
    )

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#fbfdfe")
    ax.plot(
        deflections,
        recommended_cd("Venturimeter") * q_theoretical_l_s,
        color="#008985",
        linewidth=2.7,
        label="Venturimeter (Cd = 0.98)",
    )
    ax.plot(
        deflections,
        recommended_cd("Orifice meter") * q_theoretical_l_s,
        color="#ef7d32",
        linewidth=2.7,
        label="Orifice meter (Cd = 0.62)",
    )

    current_result = calculate_discharge(data)
    ax.scatter(
        [data.manometer_deflection_mm],
        [current_result["actual_discharge_l_s"]],
        s=85,
        color="#102a43",
        edgecolor="white",
        linewidth=1.7,
        zorder=4,
        label=f"Current {data.meter_type}",
    )
    ax.set_xlabel("Manometer deflection, x (mm)", fontweight="semibold")
    ax.set_ylabel("Actual discharge, Q (L/s)", fontweight="semibold")
    ax.set_title("Discharge response for the same pipe geometry", loc="left", fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.28)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    return fig


def result_csv(data: MeterInputs, result: dict[str, float | str]) -> str:
    """Create a one-record CSV without adding a pandas dependency."""

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["FlowLab — Problem 14 result"])
    writer.writerow(["Parameter", "Value", "Unit"])
    rows = [
        ("Meter type", data.meter_type, "-"),
        ("Inlet diameter", data.inlet_diameter_mm, "mm"),
        ("Throat/orifice diameter", data.throat_diameter_mm, "mm"),
        ("Manometer deflection", data.manometer_deflection_mm, "mm"),
        ("Flowing-fluid density", data.fluid_density_kg_m3, "kg/m³"),
        ("Manometer-fluid density", data.manometer_density_kg_m3, "kg/m³"),
        ("Coefficient of discharge", data.coefficient_of_discharge, "-"),
        ("Pressure difference", f"{float(result['pressure_difference_kpa']):.5f}", "kPa"),
        ("Differential pressure head", f"{float(result['differential_head_m']):.5f}", "m of flowing liquid"),
        ("Theoretical discharge", f"{float(result['theoretical_discharge_l_s']):.5f}", "L/s"),
        ("Actual discharge", f"{float(result['actual_discharge_l_s']):.5f}", "L/s"),
        ("Inlet velocity", f"{float(result['inlet_velocity_m_s']):.5f}", "m/s"),
        ("Throat/orifice velocity", f"{float(result['throat_velocity_m_s']):.5f}", "m/s"),
    ]
    writer.writerows(rows)
    return buffer.getvalue()


apply_styles()

with st.sidebar:
    st.markdown("## Input panel")
    st.caption("Enter the meter and manometer data using the units shown.")

    st.markdown("### Meter geometry")
    meter_type = st.selectbox(
        "Meter type",
        ("Venturimeter", "Orifice meter"),
        help="A Venturimeter normally has a higher coefficient of discharge than an orifice meter.",
    )
    inlet_diameter_mm = st.number_input(
        "Inlet diameter, D₁ (mm)", min_value=1.0, max_value=2000.0, value=100.0, step=1.0
    )
    throat_diameter_mm = st.number_input(
        "Throat / orifice diameter, D₂ (mm)",
        min_value=1.0,
        max_value=1999.0,
        value=50.0,
        step=1.0,
    )

    st.markdown("### Manometer data")
    deflection_mm = st.number_input(
        "Manometer deflection, x (mm)",
        min_value=0.0,
        max_value=5000.0,
        value=200.0,
        step=5.0,
    )
    flowing_fluid = st.selectbox("Flowing liquid", (*FLOWING_FLUIDS.keys(), "Custom"))
    if flowing_fluid == "Custom":
        fluid_density = st.number_input(
            "Flowing-liquid density (kg/m³)", min_value=1.0, value=1000.0, step=10.0
        )
    else:
        fluid_density = FLOWING_FLUIDS[flowing_fluid]
        st.caption(f"Density used: {fluid_density:.0f} kg/m³")

    manometer_fluid = st.selectbox(
        "Manometer liquid", (*MANOMETER_FLUIDS.keys(), "Custom")
    )
    if manometer_fluid == "Custom":
        manometer_density = st.number_input(
            "Manometer-liquid density (kg/m³)", min_value=1.0, value=13600.0, step=10.0
        )
    else:
        manometer_density = MANOMETER_FLUIDS[manometer_fluid]
        st.caption(f"Density used: {manometer_density:.0f} kg/m³")

    cd_key = "cd_venturi" if meter_type == "Venturimeter" else "cd_orifice"
    coefficient = st.slider(
        "Coefficient of discharge, Cd",
        min_value=0.10,
        max_value=1.00,
        value=recommended_cd(meter_type),
        step=0.01,
        key=cd_key,
        help="Representative values: Venturimeter ≈ 0.98; Orifice meter ≈ 0.62.",
    )

data = MeterInputs(
    meter_type=meter_type,
    inlet_diameter_mm=float(inlet_diameter_mm),
    throat_diameter_mm=float(throat_diameter_mm),
    manometer_deflection_mm=float(deflection_mm),
    fluid_density_kg_m3=float(fluid_density),
    manometer_density_kg_m3=float(manometer_density),
    coefficient_of_discharge=float(coefficient),
)

try:
    result = calculate_discharge(data)
except ValueError as error:
    st.error(f"Input error: {error}", icon="⚠️")
    st.info("Correct the values in the input panel. The throat/orifice must be smaller than the inlet.")
    st.stop()

st.markdown(
    """
    <section class="hero">
      <div class="eyebrow">Mechanical Engineering Mini Project · Problem 14</div>
      <h1>FlowLab</h1>
      <p>Venturimeter and Orifice Meter Discharge Calculator — converts a differential-manometer reading into theoretical and actual volume flow rate.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

dashboard_tab, formula_tab, viva_tab = st.tabs(
    ["Performance dashboard", "Formula & verification", "Theory & viva"]
)

with dashboard_tab:
    st.markdown('<div class="section-kicker">Calculated output</div>', unsafe_allow_html=True)
    if data.manometer_deflection_mm == 0:
        st.warning("The pressure difference is zero, so the calculated discharge is zero.")

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Pressure difference", f"{float(result['pressure_difference_kpa']):.2f} kPa")
    metric_2.metric("Theoretical discharge", f"{float(result['theoretical_discharge_l_s']):.2f} L/s")
    metric_3.metric("Actual discharge", f"{float(result['actual_discharge_l_s']):.2f} L/s")
    metric_4.metric("Actual flow rate", f"{float(result['actual_discharge_l_min']):.1f} L/min")

    st.markdown(
        f"""
        <div class="result-note">
          <strong>{data.meter_type} result:</strong> the real discharge is
          <strong>{data.coefficient_of_discharge * 100:.1f}%</strong> of the ideal value.
          The throat/orifice velocity is <strong>{float(result['throat_velocity_m_s']):.2f} m/s</strong>,
          compared with <strong>{float(result['inlet_velocity_m_s']):.2f} m/s</strong> at the inlet.
        </div>
        """,
        unsafe_allow_html=True,
    )

    diagram_column, detail_column = st.columns([1.65, 1], gap="large")
    with diagram_column:
        components.html(meter_animation(data.meter_type, result), height=430, scrolling=False)
    with detail_column:
        st.markdown("### Flow details")
        st.metric("Differential head", f"{float(result['differential_head_m']):.3f} m")
        st.metric("Inlet velocity", f"{float(result['inlet_velocity_m_s']):.3f} m/s")
        st.metric("Throat / orifice velocity", f"{float(result['throat_velocity_m_s']):.3f} m/s")
        st.caption("Animated schematic is explanatory and is not drawn to scale.")

    st.markdown("### Venturimeter vs. orifice response")
    st.caption("The comparison uses the same pipe, liquid and manometer. Only the representative Cd changes.")
    comparison_figure = create_comparison_figure(data)
    st.pyplot(comparison_figure, use_container_width=True)
    plt.close(comparison_figure)

    summary_1, summary_2 = st.columns([1.2, 1])
    with summary_1:
        st.markdown("#### Current calculation summary")
        st.dataframe(
            {
                "Quantity": [
                    "Diameter ratio (β)",
                    "Inlet area",
                    "Throat/orifice area",
                    "Pressure head",
                    "Discharge reduction due to Cd",
                ],
                "Value": [
                    f"{float(result['beta']):.3f}",
                    f"{float(result['area_1_m2']):.6f} m²",
                    f"{float(result['area_2_m2']):.6f} m²",
                    f"{float(result['differential_head_m']):.4f} m",
                    f"{float(result['discharge_reduction_percent']):.1f}%",
                ],
            },
            hide_index=True,
            use_container_width=True,
        )
    with summary_2:
        st.markdown("#### Export result")
        st.write("Download the current inputs and calculated outputs for your report record.")
        st.download_button(
            "Download result as CSV",
            data=result_csv(data, result),
            file_name="problem14_discharge_result.csv",
            mime="text/csv",
            use_container_width=True,
        )

with formula_tab:
    st.markdown("## Formula sheet")
    st.write(
        "For a horizontal differential-pressure meter, continuity and Bernoulli's equation give the ideal discharge. The coefficient of discharge corrects the ideal result for real losses."
    )
    equation_left, equation_right = st.columns(2, gap="large")
    with equation_left:
        st.markdown('<div class="formula-card">', unsafe_allow_html=True)
        st.markdown("**1. Differential pressure and head**")
        st.latex(r"\Delta p=(\rho_m-\rho_f)g x")
        st.latex(r"h=\frac{\Delta p}{\rho_f g}=x\left(\frac{\rho_m}{\rho_f}-1\right)")
        st.markdown("**2. Cross-sectional areas**")
        st.latex(r"A_1=\frac{\pi D_1^2}{4},\qquad A_2=\frac{\pi D_2^2}{4}")
        st.markdown("</div>", unsafe_allow_html=True)
    with equation_right:
        st.markdown('<div class="formula-card">', unsafe_allow_html=True)
        st.markdown("**3. Theoretical and actual discharge**")
        st.latex(
            r"Q_{th}=\frac{A_1A_2}{\sqrt{A_1^2-A_2^2}}\sqrt{2gh}"
        )
        st.latex(r"Q_a=C_dQ_{th}")
        st.markdown("**4. Mean velocities**")
        st.latex(r"V_1=\frac{Q_a}{A_1},\qquad V_2=\frac{Q_a}{A_2}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Substitution for current inputs")
    st.code(
        "\n".join(
            [
                f"D1 = {data.inlet_diameter_mm:.1f} mm = {float(result['diameter_1_m']):.4f} m",
                f"D2 = {data.throat_diameter_mm:.1f} mm = {float(result['diameter_2_m']):.4f} m",
                f"Δp = ({data.manometer_density_kg_m3:.0f} − {data.fluid_density_kg_m3:.0f}) × 9.81 × {float(result['deflection_m']):.4f}",
                f"Δp = {float(result['pressure_difference_pa']):.2f} Pa",
                f"Qth = {float(result['theoretical_discharge_m3_s']):.6f} m³/s",
                f"Qa = {data.coefficient_of_discharge:.2f} × {float(result['theoretical_discharge_m3_s']):.6f}",
                f"Qa = {float(result['actual_discharge_m3_s']):.6f} m³/s = {float(result['actual_discharge_l_s']):.3f} L/s",
            ]
        ),
        language="text",
    )

    st.markdown("## Textbook verification case")
    verification_data = MeterInputs(
        meter_type="Venturimeter",
        inlet_diameter_mm=100.0,
        throat_diameter_mm=50.0,
        manometer_deflection_mm=200.0,
        fluid_density_kg_m3=1000.0,
        manometer_density_kg_m3=13600.0,
        coefficient_of_discharge=0.98,
    )
    verification = calculate_discharge(verification_data)
    verify_a, verify_b = st.columns(2)
    with verify_a:
        st.markdown(
            """
            <div class="info-card">
              <strong>Given values</strong><br><br>
              Water through a Venturimeter<br>
              D₁ = 100 mm, D₂ = 50 mm<br>
              Mercury deflection = 200 mm<br>
              Cd = 0.98
            </div>
            """,
            unsafe_allow_html=True,
        )
    with verify_b:
        st.success(
            f"Verified answer: Qth = {float(verification['theoretical_discharge_l_s']):.3f} L/s and Qa = {float(verification['actual_discharge_l_s']):.3f} L/s."
        )
        st.caption("Use this case for the manual calculation vs. app comparison in the report.")

with viva_tab:
    st.markdown("## Engineering interpretation")
    comparison_rows = {
        "Feature": [
            "Geometry",
            "Typical Cd used here",
            "Permanent head loss",
            "Space and cost",
            "Typical use",
        ],
        "Venturimeter": [
            "Smooth converging throat and diffuser",
            "0.98",
            "Lower",
            "Longer and more expensive",
            "Accurate flow measurement",
        ],
        "Orifice meter": [
            "Thin plate with a sharp-edged opening",
            "0.62",
            "Higher",
            "Compact and economical",
            "General industrial measurement",
        ],
    }
    st.dataframe(comparison_rows, hide_index=True, use_container_width=True)

    st.markdown("### What the result means")
    st.markdown(
        f"""
        - The manometer measures a pressure difference of **{float(result['pressure_difference_kpa']):.2f} kPa**.
        - The reduced area increases velocity from **{float(result['inlet_velocity_m_s']):.2f} m/s** to **{float(result['throat_velocity_m_s']):.2f} m/s**.
        - Because discharge is proportional to **√x**, doubling manometer deflection does **not** double the flow; it multiplies it by √2.
        - The selected coefficient changes ideal discharge to the realistic value of **{float(result['actual_discharge_l_s']):.2f} L/s**.
        """
    )

    st.markdown("### Assumptions and limitations")
    st.info(
        "Steady incompressible flow · horizontal pipe · negligible elevation difference between taps · uniform mean velocity · denser manometer liquid · no cavitation · user-supplied Cd represents real losses."
    )

    st.markdown("### Viva-ready questions")
    viva_items = [
        (
            "Why is actual discharge less than theoretical discharge?",
            "Real flow has friction, turbulence and contraction losses. Cd accounts for these effects, so Qa = Cd × Qth.",
        ),
        (
            "Why is a Venturimeter generally more accurate than an orifice meter?",
            "Its gradual converging and diverging passages reduce separation and permanent energy loss, giving a Cd close to one.",
        ),
        (
            "What happens when throat diameter decreases?",
            "For the same discharge the throat velocity rises, and a larger pressure difference is produced. Very small openings can also increase losses.",
        ),
        (
            "Why must the manometer liquid be denser here?",
            "The equation used assumes a heavier differential-manometer liquid. It produces a stable level difference for the pipe pressure difference.",
        ),
        (
            "What is the relation between discharge and manometer reading?",
            "For fixed geometry and fluids, Q is proportional to the square root of the deflection: Q ∝ √x.",
        ),
        (
            "Which principles are used in this calculation?",
            "Continuity equation, Bernoulli's equation, hydrostatic manometer relation and the coefficient of discharge.",
        ),
    ]
    for question, answer in viva_items:
        with st.expander(question):
            st.write(answer)

st.markdown("---")
members_html = "<br><br>".join(
    f"<strong>{name}</strong><br>Enrollment No. {enrollment}"
    for name, enrollment in PROJECT_MEMBERS
)
st.markdown(
    f"""
    <div class="student-card">
      <div class="section-kicker">Project members</div>
      {members_html}<br>
      <span class="small-note">Diploma in Mechanical Engineering · Semester 3 · Python & Streamlit Mini Project</span>
    </div>
    """,
    unsafe_allow_html=True,
)
