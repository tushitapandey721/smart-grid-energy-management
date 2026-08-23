import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import energy_engine

# Page Configuration
st.set_page_config(
    page_title="VoltIQ Smart Grid — AI Energy Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Neutral Theme Clean Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.5px;
    }

    .stMetricValue {
        font-family: 'JetBrains Mono', monospace !important;
        color: #2563eb !important;
    }

    /* Neutral Cards */
    .neutral-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
        margin-bottom: 16px;
    }

    .badge-status {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        margin-bottom: 8px;
        background: #ecfdf5;
        color: #059669;
        border: 1px solid rgba(5, 150, 105, 0.3);
    }

    .tip-box-neutral {
        background: #eff6ff;
        border-left: 4px solid #2563eb;
        border-radius: 6px;
        padding: 12px 16px;
        margin-top: 12px;
        font-size: 0.9rem;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# Header Banner Section with Crisp White Heading
st.markdown(f"""
<div style="background: linear-gradient(135deg, #090d16 0%, #0f172a 60%, #1e293b 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 22px 28px; margin-bottom: 20px; color: #ffffff; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 16px rgba(0,0,0,0.15);">
    <div>
        <span class="badge-status">System Online &bull; PCA-12 Dimensionality Reduction</span>
        <h1 style="color: #ffffff !important; margin: 6px 0 2px 0; font-size: 2.1rem; font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif;">VoltIQ Smart Grid Energy Management</h1>
        <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0;">AI-driven residential electricity demand forecasting, sub-metering breakdown, and grid balancing platform.</p>
    </div>
    <div style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 10px 16px; text-align: right;">
        <span style="font-size: 0.72rem; color: #94a3b8; font-weight: 600;">GRID TIME</span><br>
        <span style="font-family: 'JetBrains Mono'; font-size: 0.95rem; font-weight: 700; color: #ffffff;">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar: Presets & Controls
with st.sidebar:
    st.markdown("### Scenario Profiles")
    st.write("Select a pre-configured electrical scenario:")
    
    preset_choice = st.selectbox(
        "Load Profile",
        options=list(energy_engine.PRESETS.keys()),
        format_func=lambda k: energy_engine.PRESETS[k]["name"],
        index=4
    )
    
    preset_data = energy_engine.PRESETS[preset_choice]["data"]
    st.info(energy_engine.PRESETS[preset_choice]["description"])
    
    st.divider()
    st.markdown("### Temporal Auto-Sync")
    use_current_dt = st.checkbox("Auto-derive from current local time", value=True)
    
    if use_current_dt:
        dt_current = datetime.now()
        derived_time = energy_engine.derive_time_features(dt_current)
    else:
        selected_date = st.date_input("Select Date", datetime.now().date())
        selected_hour = st.slider("Hour of Day (0-23)", 0, 23, 18)
        dt_custom = datetime.combine(selected_date, datetime.min.time()).replace(hour=selected_hour)
        derived_time = energy_engine.derive_time_features(dt_custom)

# 4 Comprehensive Tabs (including Landing & Overview)
tab_overview, tab_predict, tab_simulator, tab_analytics = st.tabs([
    "System Overview & Working",
    "Demand Predictor Workspace",
    "Load Simulator & What-If",
    "ML Architecture & PCA"
])

# ==============================================================================
# TAB 0: System Overview & Architecture
# ==============================================================================
with tab_overview:
    st.markdown("### How the Smart Grid Demand Forecasting Pipeline Works")
    st.write("A structured machine learning system that transforms high-frequency smart meter readings into actionable load balancing and cost projections.")
    
    col_st1, col_st2, col_st3, col_st4 = st.columns(4)
    with col_st1:
        st.markdown("""
        <div class="neutral-card">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #64748b; font-weight: 700;">STAGE 01</span>
            <h4 style="margin: 8px 0; color: #0f172a;">Telemetry Ingestion</h4>
            <p style="font-size: 0.84rem; color: #475569; line-height: 1.5;">Captures 15 simultaneous inputs including voltage, current, sub-metering, and rolling averages.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_st2:
        st.markdown("""
        <div class="neutral-card">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #64748b; font-weight: 700;">STAGE 02</span>
            <h4 style="margin: 8px 0; color: #0f172a;">PCA Compression</h4>
            <p style="font-size: 0.84rem; color: #475569; line-height: 1.5;">Reduces 15 correlated dimensions into 12 orthogonal components, preserving >95% data variance.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_st3:
        st.markdown("""
        <div class="neutral-card">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #64748b; font-weight: 700;">STAGE 03</span>
            <h4 style="margin: 8px 0; color: #0f172a;">Linear Regression</h4>
            <p style="font-size: 0.84rem; color: #475569; line-height: 1.5;">Fits transformed vectors to produce high-throughput active power demand forecasts in kW.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_st4:
        st.markdown("""
        <div class="neutral-card">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #64748b; font-weight: 700;">STAGE 04</span>
            <h4 style="margin: 8px 0; color: #0f172a;">Load Optimization</h4>
            <p style="font-size: 0.84rem; color: #475569; line-height: 1.5;">Translates kW output into financial billing estimates, CO₂ emissions, and peak shaving advice.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Sub-Metering Classification")
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    with sub_col1:
        st.markdown("""
        **Sub-Metering 1 (Kitchen Zone)**  
        *Appliances:* Dishwasher, microwave, oven, kitchen auxiliaries.  
        *Pattern:* Pronounced morning and dinner spike windows.
        """)
    with sub_col2:
        st.markdown("""
        **Sub-Metering 2 (Laundry Zone)**  
        *Appliances:* Washing machine, tumble dryer, laundry heating.  
        *Pattern:* Concentrated weekend and daytime cycles. Prime target for off-peak shifting.
        """)
    with sub_col3:
        st.markdown("""
        **Sub-Metering 3 (Climate & Heating)**  
        *Appliances:* Air conditioning, electric water heater, space heating.  
        *Pattern:* Heavy continuous draw during extreme weather and evening peak hours (6–10 PM).
        """)

# ==============================================================================
# TAB 1: Demand Predictor Workspace
# ==============================================================================
with tab_predict:
    st.markdown("### Input Telemetry & Environmental Readings")
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        st.markdown("#### Electrical Telemetry")
        Voltage = st.number_input("Supply Voltage (V)", value=float(preset_data.get("Voltage", 234.84)), step=0.5)
        Global_intensity = st.number_input("Current Intensity (A)", value=float(preset_data.get("Global_intensity", 18.4)), step=0.1)
        Global_reactive_power = st.number_input("Global Reactive Power (kVAR)", value=float(preset_data.get("Global_reactive_power", 0.418)), step=0.01)
        
    with col_e2:
        st.markdown("#### Sub-Metering Loads (Wh)")
        Sub_metering_1 = st.number_input("Sub 1: Kitchen (Wh)", value=float(preset_data.get("Sub_metering_1", 0.0)), step=1.0)
        Sub_metering_2 = st.number_input("Sub 2: Laundry (Wh)", value=float(preset_data.get("Sub_metering_2", 1.0)), step=1.0)
        Sub_metering_3 = st.number_input("Sub 3: HVAC / Boiler (Wh)", value=float(preset_data.get("Sub_metering_3", 17.0)), step=1.0)
        
    with col_e3:
        st.markdown("#### Baseline & Temporal Context")
        Previous_Power = st.number_input("Previous Minute Power (kW)", value=float(preset_data.get("Previous_Power", 4.216)), step=0.1)
        Rolling_Mean_24 = st.number_input("24h Rolling Mean Power (kW)", value=float(preset_data.get("Rolling_Mean_24", 1.091)), step=0.1)
        
        st.caption(f"Hour: {derived_time['Hour']} | Day: {derived_time['Day']} | Month: {derived_time['Month']} | Year: {derived_time['Year']}")
        st.caption(f"Weekend: {'Yes' if derived_time['Weekend'] == 1 else 'No'} | Peak Period (6-10 PM): {'Yes' if derived_time['Peak_Hour'] == 1 else 'No'}")

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

    analytics = energy_engine.predict_consumption(input_payload)
    pred_kw = analytics["predicted_kw"]
    
    st.markdown("---")
    st.markdown("### Demand Forecasting Results & Analytics")
    
    res_col_left, res_col_right = st.columns([1.2, 2])
    
    with res_col_left:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pred_kw,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "<b>Predicted Active Demand</b>", 'font': {'size': 16, 'color': '#0f172a', 'family': 'Plus Jakarta Sans'}},
            number={'suffix': " kW", 'font': {'size': 32, 'color': '#2563eb', 'family': 'JetBrains Mono'}},
            gauge={
                'axis': {'range': [0, 6], 'tickwidth': 1, 'tickcolor': "#64748b"},
                'bar': {'color': analytics["tier_color"], 'thickness': 0.3},
                'bgcolor': "#f8fafc",
                'borderwidth': 1,
                'bordercolor': "#e2e8f0",
                'steps': [
                    {'range': [0, 1.2], 'color': "rgba(5, 150, 105, 0.15)"},
                    {'range': [1.2, 3.2], 'color': "rgba(217, 119, 6, 0.15)"},
                    {'range': [3.2, 6.0], 'color': "rgba(220, 38, 38, 0.15)"}
                ],
                'threshold': {
                    'line': {'color': "#dc2626", 'width': 3},
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
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric(
                label="Efficiency Tier",
                value=analytics["tier"],
                delta="Normal Off-Peak" if derived_time["Peak_Hour"] == 0 else "Peak Tariff Period",
                delta_color="normal" if derived_time["Peak_Hour"] == 0 else "inverse"
            )
            st.metric(
                label="Hourly Cost Estimate",
                value=f"${analytics['hourly_cost_usd']:.3f}",
                delta=f"INR {analytics['hourly_cost_inr']:.2f} / hr"
            )
            
        with m_col2:
            st.metric(
                label="Projected Monthly Consumption",
                value=f"{analytics['monthly_estimate_kwh']} kWh",
                delta=f"~${analytics['monthly_cost_usd']} / month"
            )
            st.metric(
                label="Carbon Emissions",
                value=f"{analytics['carbon_kg_hr']} kg CO₂/hr",
                delta="Factor: 0.475 kg/kWh"
            )

        st.markdown(f"""
        <div class="tip-box-neutral">
            <strong>Advisory:</strong> {analytics['tier_advice']}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        st.markdown("#### Appliance Sub-Metering Breakdown")
        bd = analytics["breakdown"]
        labels = ['Kitchen (Sub 1)', 'Laundry (Sub 2)', 'HVAC / Heating (Sub 3)', 'Baseline Load']
        values = [bd['kitchen_pct'], bd['laundry_pct'], bd['hvac_pct'], bd['base_pct']]
        colors = ['#2563eb', '#7c3aed', '#d97706', '#059669']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.6,
            marker=dict(colors=colors, line=dict(color='#ffffff', width=2))
        )])
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(font=dict(color="#475569", size=11), orientation="h", y=-0.1)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with c_col2:
        st.markdown("#### Simulated 24-Hour Load Profile")
        hours = list(range(24))
        fig_line = px.area(
            x=hours,
            y=analytics["simulated_24h"],
            labels={'x': 'Hour of Day (0-23)', 'y': 'Predicted Demand (kW)'},
        )
        fig_line.update_traces(line_color='#2563eb', fillcolor='rgba(37, 99, 235, 0.1)')
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor="#f1f5f9", color="#64748b"),
            yaxis=dict(gridcolor="#f1f5f9", color="#64748b")
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ==============================================================================
# TAB 2: Load Simulator & What-If Optimizer
# ==============================================================================
with tab_simulator:
    st.markdown("### Interactive 'What-If' Energy Simulator")
    st.write("Simulate the demand and cost impact of adjusting appliance usage or rescheduling cycles away from peak hours.")
    
    sim_col1, sim_col2 = st.columns(2)
    
    with sim_col1:
        st.markdown("#### Appliance Overrides")
        hvac_toggle = st.slider("HVAC / Water Heater Load (Wh)", 0.0, 40.0, float(Sub_metering_3), step=1.0)
        laundry_toggle = st.slider("Laundry Load (Wh)", 0.0, 40.0, float(Sub_metering_2), step=1.0)
        shift_off_peak = st.checkbox("Reschedule load to Off-Peak Hour (2:00 PM)", value=False)
        
    with sim_col2:
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
            label="Simulated Active Demand",
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
            st.success(f"Optimized schedule reduces emissions by approx. {abs(delta_kw)*24*30.5*0.475:.1f} kg CO₂ per month.")

# ==============================================================================
# TAB 3: ML & PCA Architecture
# ==============================================================================
with tab_analytics:
    st.markdown("### Model Diagnostics & Dimensionality Analysis")
    
    arch_col1, arch_col2 = st.columns(2)
    with arch_col1:
        st.markdown("""
        #### Pipeline Breakdown
        1. **SimpleImputer:** Imputes missing telemetry values using column medians.
        2. **StandardScaler:** Normalizes feature distributions to zero mean & unit variance.
        3. **PCA (Principal Component Analysis):** Compresses **15 input dimensions** down to **12 orthogonal components**, capturing >95% explained variance and eliminating collinearity between current, voltage, and sub-metering.
        4. **Linear Regression:** High-throughput linear model predicting continuous active power output in kilowatts (kW).
        """)
        
    with arch_col2:
        st.markdown("#### PCA Components Summary")
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