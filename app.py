import pandas as pd
import streamlit as st
from utils.simulation import simulate_sensor_input
from utils.ai_engine import analyze_water_data

# 1. Page Configuration
st.set_page_config(
    page_title="AI Water Quality Monitoring Dashboard",
    page_icon="💧",
    layout="wide"
)

st.title("💧 AI-Driven Water Quality Monitoring Dashboard")
st.markdown("A software prototype for simulated or manually entered water measurements, analysis, and quality evaluation.")

# 2. Sidebar Controls for Input Settings
st.sidebar.header("Input Settings")
simulation_mode = st.sidebar.radio(
    "Mode",
    ["Live Stream (Auto-refresh)", "Manual Input"]
)
if simulation_mode == "Live Stream (Auto-refresh)":
    refresh_rate = st.sidebar.slider("Refresh Interval (seconds)", 1, 5, 2)

def display_analysis(ph, turbidity, tds, chart_title="📈 Real-Time Parameter Telemetry Stream"):
    status, wqi_score, warnings = analyze_water_data(ph, turbidity, tds)

    # Status Banner
    if status == "OPTIMAL":
        st.success(f"**System Status: {status}** (Water Quality Index: {wqi_score}/100)")
    elif status == "WARNING":
        st.warning(f"**System Status: {status}** (Water Quality Index: {wqi_score}/100)")
    else:
        st.error(f"**System Status: {status}** (Water Quality Index: {wqi_score}/100)")

    # Metric Cards Columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("pH Level", f"{ph}", delta="Target: 6.5 - 8.5", delta_color="normal")
    col2.metric("Turbidity", f"{turbidity} NTU", delta="Max: 5.0 NTU", delta_color="inverse")
    col3.metric("TDS", f"{tds} ppm", delta="Max: 500 ppm", delta_color="inverse")
    col4.metric("AI Health WQI", f"{wqi_score} / 100", delta="Score")

    # Active Alerts Section
    st.subheader("🤖 AI Insights & Active Alerts")
    if warnings:
        for warning in warnings:
            st.error(f"⚠️ {warning}")
    else:
        st.info("✨ All parameters are running within optimal AI-predicted thresholds. No anomalies detected.")

    # Historical Trend Chart Mockup
    st.subheader(chart_title)
    chart_data = pd.DataFrame({
        "pH": [ph - 0.2, ph - 0.1, ph],
        "Turbidity (NTU)": [turbidity - 0.5, turbidity - 0.2, turbidity],
        "TDS (ppm)": [tds - 10, tds - 5, tds]
    })
    st.line_chart(chart_data)

def run_dashboard_loop():
    data = simulate_sensor_input()
    display_analysis(data["ph"], data["turbidity_ntu"], data["tds_ppm"])

if simulation_mode == "Manual Input":
    st.subheader("Enter Water Measurements")
    with st.form("manual_water_quality_form"):
        ph_input, turbidity_input, tds_input = st.columns(3)
        ph = ph_input.number_input(
            "pH level",
            min_value=0.0,
            max_value=14.0,
            value=7.0,
            step=0.1
        )
        turbidity = turbidity_input.number_input(
            "Turbidity (NTU)",
            min_value=0.0,
            value=1.0,
            step=0.1
        )
        tds = tds_input.number_input(
            "TDS (ppm)",
            min_value=0.0,
            value=250.0,
            step=1.0
        )
        analyze_submitted = st.form_submit_button("Analyze readings")

    if analyze_submitted:
        st.session_state["manual_water_reading"] = {
            "ph": ph,
            "turbidity": turbidity,
            "tds": tds
        }

    if "manual_water_reading" in st.session_state:
        reading = st.session_state["manual_water_reading"]
        display_analysis(
            reading["ph"],
            reading["turbidity"],
            reading["tds"],
            chart_title="📈 Illustrative Values (not historical readings)"
        )
else:
    @st.fragment(run_every=refresh_rate)
    def run_live_dashboard():
        run_dashboard_loop()

    run_live_dashboard()