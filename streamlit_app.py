import streamlit as st
import streamlit.components.v1 as components
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

# 1. Interactive Generative Electric Wave Hero Banner (HTML5 Canvas Component)
hero_canvas_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=JetBrains+Mono:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #090d16;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            overflow: hidden;
            border-radius: 14px;
            position: relative;
            user-select: none;
        }}
        #waveCanvas {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 1;
            cursor: crosshair;
        }}
        .hero-overlay {{
            position: relative;
            z-index: 2;
            padding: 24px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            pointer-events: none;
            background: linear-gradient(90deg, rgba(9,13,22,0.85) 0%, rgba(9,13,22,0.4) 60%, rgba(9,13,22,0.85) 100%);
            height: 180px;
        }}
        .hero-left h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 2.0rem;
            font-weight: 800;
            color: #ffffff;
            text-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
            margin-bottom: 4px;
        }}
        .hero-left p {{
            font-size: 0.88rem;
            color: #cbd5e1;
            max-width: 600px;
        }}
        .badge {{
            display: inline-block;
            background: rgba(0, 242, 254, 0.15);
            border: 1px solid rgba(0, 242, 254, 0.35);
            color: #00f2fe;
            padding: 3px 10px;
            border-radius: 14px;
            font-size: 0.72rem;
            font-weight: 700;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }}
        .hero-right {{
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(0, 242, 254, 0.25);
            border-radius: 10px;
            padding: 12px 18px;
            text-align: right;
            backdrop-filter: blur(10px);
        }}
        .clock-label {{
            font-size: 0.7rem;
            color: #94a3b8;
            letter-spacing: 0.5px;
        }}
        .clock-val {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.05rem;
            font-weight: 700;
            color: #ffffff;
        }}
        .wave-hint {{
            position: absolute;
            bottom: 8px;
            left: 30px;
            font-size: 0.7rem;
            color: rgba(255,255,255,0.4);
            z-index: 2;
            pointer-events: none;
        }}
    </style>
</head>
<body>
    <canvas id="waveCanvas"></canvas>
    <div class="hero-overlay">
        <div class="hero-left">
            <span class="badge"><i class="fa-solid fa-wave-square"></i> INTERACTIVE ELECTRIC WAVE ENGINE</span>
            <h1>VoltIQ Smart Grid Energy Management</h1>
            <p>AI-driven residential electricity demand forecasting, sub-metering decomposition, and real-time grid load balancing.</p>
        </div>
        <div class="hero-right">
            <span class="clock-label">GRID TIME</span><br>
            <span class="clock-val">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
        </div>
    </div>
    <div class="wave-hint"><i class="fa-solid fa-arrow-pointer"></i> Move your cursor across the canvas to interact with electric wave physics</div>

    <script>
        const canvas = document.getElementById('waveCanvas');
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = 180;

        let mouse = {{ x: width / 2, y: height / 2, targetX: width / 2, targetY: height / 2 }};
        let time = 0;

        const waves = [
            {{ amplitude: 35, frequency: 0.008, speed: 0.025, color: 'rgba(56, 189, 248, 0.45)', lineWidth: 2.5, phase: 0 }},
            {{ amplitude: 25, frequency: 0.012, speed: 0.035, color: 'rgba(0, 242, 254, 0.6)', lineWidth: 2.0, phase: 2 }},
            {{ amplitude: 40, frequency: 0.006, speed: 0.018, color: 'rgba(16, 185, 129, 0.45)', lineWidth: 2.0, phase: 4 }},
            {{ amplitude: 20, frequency: 0.016, speed: 0.03, color: 'rgba(99, 102, 241, 0.35)', lineWidth: 1.5, phase: 1 }}
        ];

        let particles = [];
        for (let i = 0; i < 35; i++) {{
            particles.push({{
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 2 + 1,
                vx: (Math.random() - 0.5) * 0.8,
                vy: (Math.random() - 0.5) * 0.8,
                alpha: Math.random() * 0.7 + 0.3,
                color: Math.random() > 0.4 ? '#00f2fe' : '#10b981'
            }});
        }}

        window.addEventListener('resize', () => {{
            width = canvas.width = window.innerWidth;
            height = canvas.height = 180;
        }});

        window.addEventListener('mousemove', (e) => {{
            const rect = canvas.getBoundingClientRect();
            mouse.targetX = e.clientX - rect.left;
            mouse.targetY = e.clientY - rect.top;
        }});

        function animate() {{
            ctx.clearRect(0, 0, width, height);
            time += 1;
            mouse.x += (mouse.targetX - mouse.x) * 0.06;
            mouse.y += (mouse.targetY - mouse.y) * 0.06;

            waves.forEach((w, idx) => {{
                ctx.beginPath();
                ctx.lineWidth = w.lineWidth;
                ctx.strokeStyle = w.color;
                ctx.shadowColor = w.color;
                ctx.shadowBlur = 10;

                const baseH = height * 0.5 + (idx - 1.5) * 16;
                for (let x = 0; x <= width; x += 5) {{
                    const dx = x - mouse.x;
                    const dy = baseH - mouse.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    const influence = Math.max(0, 1 - dist / 180) * 35;

                    const y = baseH + Math.sin(x * w.frequency + time * w.speed + w.phase) * w.amplitude - influence * Math.sin(time * 0.05);
                    if (x === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }}
                ctx.stroke();
                ctx.shadowBlur = 0;
            }});

            particles.forEach(p => {{
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0) p.x = width; if (p.x > width) p.x = 0;
                if (p.y < 0) p.y = height; if (p.y > height) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.shadowColor = p.color;
                ctx.shadowBlur = 6;
                ctx.globalAlpha = p.alpha;
                ctx.fill();
                ctx.globalAlpha = 1.0;
                ctx.shadowBlur = 0;
            }});

            for (let i = 0; i < particles.length; i++) {{
                for (let j = i + 1; j < particles.length; j++) {{
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 80) {{
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(0, 242, 254, ${{0.2 * (1 - dist / 80)}})`;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }}
                }}
            }}

            requestAnimationFrame(animate);
        }}
        animate();
    </script>
</body>
</html>
"""

components.html(hero_canvas_html, height=195, scrolling=False)

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

# 4 Comprehensive Tabs
tab_overview, tab_circuit, tab_predict, tab_simulator, tab_analytics = st.tabs([
    "System Overview & Working",
    "Interactive Circuit Simulation",
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
        *Pattern:* Heavy continuous draw during extreme weather and evening peak hours (6 to 10 PM).
        """)

# ==============================================================================
# TAB 1: Interactive Circuit Board Component
# ==============================================================================
with tab_circuit:
    st.markdown("### Interactive Household Circuit & Energy Flow Map")
    st.caption("Live electron current simulation from the grid substation into household sub-metered appliances.")
    
    circuit_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&family=JetBrains+Mono:wght@600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
            body { background: #0f172a; color: #ffffff; padding: 24px; border-radius: 14px; }
            .board { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
            .node {
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(0,242,254,0.3);
                border-radius: 12px;
                padding: 18px 22px;
                text-align: center;
                min-width: 170px;
                transition: transform 0.2s;
            }
            .node:hover { transform: translateY(-3px); border-color: #00f2fe; box-shadow: 0 0 20px rgba(0,242,254,0.3); }
            .node i { font-size: 24px; color: #00f2fe; margin-bottom: 8px; }
            .node strong { display: block; font-size: 0.95rem; }
            .node small { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94a3b8; }
            .wire { flex: 1; height: 3px; background: rgba(255,255,255,0.15); position: relative; overflow: hidden; }
            .pulse { position: absolute; top: -4px; width: 12px; height: 12px; border-radius: 50%; background: #00f2fe; box-shadow: 0 0 12px #00f2fe; animation: flow 2s linear infinite; }
            .pulse.delay { animation-delay: 1s; }
            @keyframes flow { 0% { left: -10%; opacity: 0; } 20% { opacity: 1; } 80% { opacity: 1; } 100% { left: 110%; opacity: 0; } }
            .branches { display: flex; flex-direction: column; gap: 10px; min-width: 220px; }
            .app-card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 8px 12px; display: flex; align-items: center; gap: 10px; }
            .app-card i { color: #00f2fe; }
            .app-card strong { font-size: 0.82rem; }
        </style>
    </head>
    <body>
        <div class="board">
            <div class="node">
                <i class="fa-solid fa-tower-observation"></i>
                <strong>Substation Grid</strong>
                <small>230V / 50Hz</small>
            </div>
            <div class="wire"><div class="pulse"></div></div>
            <div class="node">
                <i class="fa-solid fa-gauge-high"></i>
                <strong>Smart Meter IoT</strong>
                <small>Active Hub</small>
            </div>
            <div class="wire"><div class="pulse delay"></div></div>
            <div class="branches">
                <div class="app-card"><i class="fa-solid fa-utensils"></i> <div><strong>Kitchen (Sub 1)</strong></div></div>
                <div class="app-card"><i class="fa-solid fa-shirt"></i> <div><strong>Laundry (Sub 2)</strong></div></div>
                <div class="app-card"><i class="fa-solid fa-temperature-arrow-up"></i> <div><strong>HVAC / Heating (Sub 3)</strong></div></div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(circuit_html, height=190, scrolling=False)

# ==============================================================================
# TAB 2: Demand Predictor Workspace
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
# TAB 3: Load Simulator & What-If Optimizer
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
# TAB 4: ML & PCA Architecture
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