import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import energy_engine

# --- Page Configuration ---
st.set_page_config(
    page_title="VoltIQ Smart Grid — AI Power Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Dark Glassmorphism CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600;700&family=Outfit:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.5px;
    }

    .stMetricValue {
        font-family: 'JetBrains Mono', monospace !important;
        color: #00f2fe !important;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        backdrop-filter: blur(16px);
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }

    .glow-header {
        background: linear-gradient(135deg, #00f2fe 0%, #38bdf8 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    .badge-status {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    
    .badge-online {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .tip-box {
        background: rgba(56, 189, 248, 0.08);
        border-left: 4px solid #00f2fe;
        border-radius: 8px;
        padding: 14px 18px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Banner ---
col_head_left, col_head_right = st.columns([3, 1])

with col_head_left:
    st.markdown('<span class="badge-status badge-online">● SYSTEM ACTIVE | PCA-12 COMPRESSION</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="glow-header">⚡ VoltIQ Smart Grid Energy Management</h1>', unsafe_allow_html=True)
    st.caption("AI-powered household electricity consumption prediction and smart load balancing engine.")

with col_head_right:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0,242,254,0.2); border-radius: 12px; padding: 12px; text-align: right;">
        <span style="font-size: 0.75rem; color: #94a3b8;">GRID SYNCHRONIZATION</span><br>
        <span style="font-family: 'JetBrains Mono'; font-size: 1.05rem; font-weight: 700; color: #f8fafc;">{now_str}</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- Sidebar: Presets & Controls ---
with st.sidebar:
    st.markdown("### 🎛️ Scenario Presets")
    st.write("Pick a preset electrical profile:")
    
    preset_choice = st.selectbox(
        "Load Preset Profile",
        options=list(energy_engine.PRESETS.keys()),
        format_func=lambda k: energy_engine.PRESETS[k]["name"],
        index=4
    )
    
    preset_data = energy_engine.PRESETS[preset_choice]["data"]
    st.info(energy_engine.PRESETS[preset_choice]["description"])
    
    st.divider()
    st.markdown("### 🕒 Auto Time Sync")
    use_current_dt = st.checkbox("Auto-derive from current time", value=True)
    
    if use_current_dt:
        dt_current = datetime.now()
        derived_time = energy_engine.derive_time_features(dt_current)
    else:
        selected_date = st.date_input("Select Date", datetime.now().date())
        selected_hour = st.slider("Hour of Day (0-23)", 0, 23, 18)
        dt_custom = datetime.combine(selected_date, datetime.min.time()).replace(hour=selected_hour)
        derived_time = energy_engine.derive_time_features(dt_custom)

# --- Main Tabs ---
tab_predict, tab_simulator, tab_analytics = st.tabs([
    "⚡ Live Power Predictor",
    "📈 Load Simulator & What-If",
    "🧠 ML & PCA Architecture"
])

# ==============================================================================
# TAB 1: Live Power Predictor
# ==============================================================================
with tab_predict:
    st.markdown("### 🔢 Enter Electrical & Sub-Metering Readings")
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        st.markdown("#### ⚙️ Electrical Telemetry")
        Voltage = st.number_input("Supply Voltage (V)", value=float(preset_data.get("Voltage", 234.84)), step=0.5, help="Standard grid voltage (usually 220–240 V)")
        Global_intensity = st.number_input("Current Intensity (A)", value=float(preset_data.get("Global_intensity", 18.4)), step=0.1, help="Total household current draw in Amperes")
        Global_reactive_power = st.number_input("Global Reactive Power (kVAR)", value=float(preset_data.get("Global_reactive_power", 0.418)), step=0.01, help="Standby / inductive reactive power")
        
    with col_e2:
        st.markdown("#### 🏠 Sub-Metering Appliance Loads (Wh)")
        Sub_metering_1 = st.number_input("Sub 1: Kitchen (Wh)", value=float(preset_data.get("Sub_metering_1", 0.0)), step=1.0, help="Microwave, oven, dishwasher")
        Sub_metering_2 = st.number_input("Sub 2: Laundry (Wh)", value=float(preset_data.get("Sub_metering_2", 1.0)), step=1.0, help="Washing machine, tumble dryer")
        Sub_metering_3 = st.number_input("Sub 3: HVAC / Water Heater (Wh)", value=float(preset_data.get("Sub_metering_3", 17.0)), step=1.0, help="Electric water boiler, air conditioning")
        
    with col_e3:
        st.markdown("#### 🕒 Baseline & Temporal Context")
        Previous_Power = st.number_input("Previous Minute Power (kW)", value=float(preset_data.get("Previous_Power", 4.216)), step=0.1)
        Rolling_Mean_24 = st.number_input("24h Rolling Mean Power (kW)", value=float(preset_data.get("Rolling_Mean_24", 1.091)), step=0.1)
        
        # Display derived time
        st.caption(f"**Hour:** {derived_time['Hour']} | **Day:** {derived_time['Day']} | **Month:** {derived_time['Month']} | **Year:** {derived_time['Year']}")
        st.caption(f"**Weekend:** {'Yes' if derived_time['Weekend'] == 1 else 'No'} | **Peak Period (6-10PM):** {'Yes' if derived_time['Peak_Hour'] == 1 else 'No'}")

    input_payload = {
        "Global_reactive_power": Global_reactive_power,
        "Voltage": Voltage,
        "Global_intensity": Global_intensity,
        "Sub_metering_1": Sub_metering_1,
        "Sub_metering_2": Sub_metering_2,
        "Sub_metering_3": Sub_metering_3,
        "Hour": derived_time["Hour"],
        "Day": derived_time["Day"],
        "Month": derived_time["Month"],
        "Year": derived_time["Year"],
        "Weekday": derived_time["Weekday"],
        "Weekend": derived_time["Weekend"],
        "Peak_Hour": derived_time["Peak_Hour"],
        "Previous_Power": Previous_Power,
        "Rolling_Mean_24": Rolling_Mean_24
    }

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Run Prediction
    analytics = energy_engine.predict_consumption(input_payload)
    pred_kw = analytics["predicted_kw"]
    
    st.markdown("---")
    st.markdown("### 📊 Prediction Results & Energy Intelligence")
    
    # Results Row: Gauge + Key Metric Tiles
    res_col_left, res_col_right = st.columns([1.2, 2])
    
    with res_col_left:
        # Plotly Radial Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pred_kw,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "<b>Predicted Active Demand</b>", 'font': {'size': 18, 'color': '#f8fafc', 'family': 'Outfit'}},
            number={'suffix': " kW", 'font': {'size': 32, 'color': '#00f2fe', 'family': 'JetBrains Mono'}},
            gauge={
                'axis': {'range': [0, 6], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                'bar': {'color': analytics["tier_color"], 'thickness': 0.3},
                'bgcolor': "rgba(15, 23, 42, 0.6)",
                'borderwidth': 1,
                'bordercolor': "rgba(255, 255, 255, 0.1)",
                'steps': [
                    {'range': [0, 1.2], 'color': "rgba(16, 185, 129, 0.25)"},
                    {'range': [1.2, 3.2], 'color': "rgba(245, 158, 11, 0.25)"},
                    {'range': [3.2, 6.0], 'color': "rgba(239, 68, 68, 0.25)"}
                ],
                'threshold': {
                    'line': {'color': "#ef4444", 'width': 3},
                    'thickness': 0.75,
                    'value': 3.2
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=260,
            margin=dict(l=20, r=20, t=40, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with res_col_right:
        # 4 Metric Cards
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric(
                label="⚡ Efficiency Tier",
                value=analytics["tier"],
                delta="Normal Off-Peak" if derived_time["Peak_Hour"] == 0 else "Peak Tariff Period",
                delta_color="normal" if derived_time["Peak_Hour"] == 0 else "inverse"
            )
            st.metric(
                label="💵 Hourly Cost Estimate",
                value=f"${analytics['hourly_cost_usd']:.3f}",
                delta=f"₹{analytics['hourly_cost_inr']:.2f} / hr"
            )
            
        with m_col2:
            st.metric(
                label="📅 Projected Monthly Consumption",
                value=f"{analytics['monthly_estimate_kwh']} kWh",
                delta=f"~${analytics['monthly_cost_usd']} / month"
            )
            st.metric(
                label="🌱 Carbon Footprint",
                value=f"{analytics['carbon_kg_hr']} kg CO₂/hr",
                delta="Emission Factor: 0.475 kg/kWh"
            )

        st.markdown(f"""
        <div class="tip-box">
            <strong>💡 Smart Energy Advisory:</strong> {analytics['tier_advice']}
        </div>
        """, unsafe_allow_html=True)

    # Charts Row: Donut + 24H Profile
    st.markdown("<br>", unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        st.markdown("#### 🥧 Sub-Metering Share")
        bd = analytics["breakdown"]
        labels = ['Kitchen (Sub 1)', 'Laundry (Sub 2)', 'HVAC / Boiler (Sub 3)', 'Baseline / Other']
        values = [bd['kitchen_pct'], bd['laundry_pct'], bd['hvac_pct'], bd['base_pct']]
        colors = ['#38bdf8', '#a855f7', '#f59e0b', '#10b981']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.6,
            marker=dict(colors=colors, line=dict(color='#0f172a', width=2))
        )])
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(font=dict(color="#94a3b8", size=11), orientation="h", y=-0.1)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with c_col2:
        st.markdown("#### 📈 Simulated 24-Hour Load Curve")
        hours = list(range(24))
        fig_line = px.area(
            x=hours,
            y=analytics["simulated_24h"],
            labels={'x': 'Hour of Day (0-23)', 'y': 'Predicted Load (kW)'},
        )
        fig_line.update_traces(line_color='#00f2fe', fillcolor='rgba(0, 242, 254, 0.15)')
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#94a3b8"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#94a3b8")
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ==============================================================================
# TAB 2: Load Simulator & What-If Optimizer
# ==============================================================================
with tab_simulator:
    st.markdown("### 🎛️ Interactive 'What-If' Energy Simulator")
    st.write("Simulate the impact of turning off high-draw appliances or shifting laundry cycles to off-peak periods.")
    
    sim_col1, sim_col2 = st.columns(2)
    
    with sim_col1:
        st.markdown("#### Appliance Overrides")
        hvac_toggle = st.slider("HVAC / Water Heater Load (Wh)", 0.0, 40.0, float(Sub_metering_3), step=1.0)
        laundry_toggle = st.slider("Laundry Load (Wh)", 0.0, 40.0, float(Sub_metering_2), step=1.0)
        shift_off_peak = st.checkbox("Shift load to Off-Peak Hour (e.g. 2:00 PM)", value=False)
        
    with sim_col2:
        # Clone inputs and evaluate delta
        sim_inputs = dict(input_payload)
        sim_inputs["Sub_metering_3"] = hvac_toggle
        sim_inputs["Sub_metering_2"] = laundry_toggle
        if shift_off_peak:
            sim_inputs["Hour"] = 14
            sim_inputs["Peak_Hour"] = 0
            
        sim_result = energy_engine.predict_consumption(sim_inputs)
        sim_kw = sim_result["predicted_kw"]
        delta_kw = sim_kw - pred_kw
        delta_cost_mo = sim_result["monthly_cost_usd"] - analytics["monthly_cost_usd"]
        
        st.markdown("#### Simulated Impact vs Baseline")
        st.metric(
            label="Simulated Demand",
            value=f"{sim_kw:.3f} kW",
            delta=f"{delta_kw:+.3f} kW",
            delta_color="inverse"
        )
        st.metric(
            label="Projected Monthly Bill Delta",
            value=f"${sim_result['monthly_cost_usd']:.2f}",
            delta=f"${delta_cost_mo:+.2f} / month",
            delta_color="inverse"
        )
        
        if delta_kw < -0.1:
            st.success(f"🌱 Excellent! This optimization saves approximately {abs(delta_kw)*24*30.5*0.475:.1f} kg of CO₂ per month.")

# ==============================================================================
# TAB 3: ML & PCA Architecture
# ==============================================================================
with tab_analytics:
    st.markdown("### 🧠 Model Architecture & Pipeline Diagnostics")
    
    arch_col1, arch_col2 = st.columns(2)
    with arch_col1:
        st.markdown("""
        #### 🏗️ Pipeline Breakdown
        1. **SimpleImputer:** Imputes missing telemetry values using column medians.
        2. **StandardScaler:** Normalizes feature distributions to zero mean & unit variance.
        3. **PCA (Principal Component Analysis):** Compresses **15 input dimensions** down to **12 orthogonal components**, capturing >95% explained variance and eliminating collinearity between current, voltage, and sub-metering.
        4. **Linear Regression:** High-throughput linear model predicting continuous active power output in kilowatts (kW).
        """)
        
    with arch_col2:
        st.markdown("#### 📐 PCA Components Summary")
        pca_obj = energy_engine.pca
        var_ratios = pca_obj.explained_variance_ratio_
        df_pca = pd.DataFrame({
            "Component": [f"PC {i+1}" for i in range(len(var_ratios))],
            "Explained Variance Ratio": var_ratios,
            "Cumulative Variance": np.cumsum(var_ratios)
        })
        st.dataframe(df_pca.style.format({
            "Explained Variance Ratio": "{:.2%}",
            "Cumulative Variance": "{:.2%}"
        }), use_container_width=True)