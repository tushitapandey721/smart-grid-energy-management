import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import energy_engine

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="VoltIQ Smart Grid — AI Energy Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# Centralized Design System & Global Stylesheet
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');

    :root {
        --grid-void: #090d16;
        --grid-panel: #0f172a;
        --current-cyan: #00f2fe;
        --current-blue: #2563eb;
        --tier-good: #059669;
        --tier-warn: #d97706;
        --tier-danger: #dc2626;
        --panel-white: #ffffff;
        --panel-border: #e2e8f0;
        --ink-slate: #0f172a;
        --ink-muted: #475569;
        --bg-subtle: #f8fafc;
    }

    /* Base Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--ink-slate);
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--ink-slate);
    }

    /* Streamlit Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid var(--panel-border);
        padding-bottom: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 0.92rem;
        padding: 10px 18px;
        border-radius: 8px 8px 0 0;
        color: var(--ink-muted);
        border: none;
        background: transparent;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        color: var(--current-blue) !important;
        background: #eff6ff !important;
        border-bottom: 3px solid var(--current-blue) !important;
    }

    /* Numeric Precision Font */
    .stMetricValue, [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        color: var(--current-blue) !important;
    }

    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }

    /* Standardized Light Instrument Card */
    .neutral-card {
        background: var(--panel-white);
        border: 1px solid var(--panel-border);
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.05);
        margin-bottom: 18px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .neutral-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(15, 23, 42, 0.08);
    }

    .card-header-mono {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748b;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
    }

    .card-title-jakarta {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--ink-slate);
        margin-bottom: 12px;
    }

    /* Mono Pill Badges */
    .badge-mono {
        font-family: 'JetBrains Mono', monospace;
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    .badge-mono-blue {
        background: #eff6ff;
        color: var(--current-blue);
        border: 1px solid #bfdbfe;
    }

    .badge-mono-green {
        background: #ecfdf5;
        color: var(--tier-good);
        border: 1px solid #a7f3d0;
    }

    .badge-mono-amber {
        background: #fffbeb;
        color: var(--tier-warn);
        border: 1px solid #fde68a;
    }

    .badge-mono-slate {
        background: #f1f5f9;
        color: #475569;
        border: 1px solid #cbd5e1;
    }

    /* Advisory Callout Box */
    .tip-box-neutral {
        background: #f0fdf4;
        border-left: 4px solid var(--tier-good);
        border-radius: 8px;
        padding: 14px 18px;
        margin-top: 14px;
        font-size: 0.9rem;
        color: #1e293b;
        line-height: 1.5;
    }

    .tip-box-neutral.warn {
        background: #fffbeb;
        border-left-color: var(--tier-warn);
    }

    .tip-box-neutral.danger {
        background: #fef2f2;
        border-left-color: var(--tier-danger);
    }

    /* Pipeline Sequence Cards & Connectors */
    .pipeline-container {
        display: flex;
        gap: 16px;
        align-items: stretch;
        margin: 16px 0 24px 0;
        position: relative;
    }

    @media (max-width: 900px) {
        .pipeline-container {
            flex-direction: column;
        }
    }

    .pipeline-step {
        flex: 1;
        background: var(--panel-white);
        border: 1px solid var(--panel-border);
        border-radius: 12px;
        padding: 20px;
        position: relative;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .pipeline-step:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 14px rgba(15, 23, 42, 0.08);
        border-color: #cbd5e1;
    }

    .pipeline-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--current-blue);
        background: #eff6ff;
        border: 1px solid #dbeafe;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 8px;
    }

    .pipeline-step h4 {
        font-size: 1.02rem;
        margin: 4px 0 8px 0;
        color: var(--ink-slate);
    }

    .pipeline-step p {
        font-size: 0.84rem;
        color: var(--ink-muted);
        line-height: 1.5;
        margin: 0;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid var(--panel-border);
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# Sidebar: Presets, Scenario Controls & Time Sync
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <span class="badge-mono badge-mono-blue"><i class="fa-solid fa-microchip"></i> VOLTIQ CONTROL PANEL</span>
        <h3 style="margin: 6px 0 2px 0; font-size: 1.25rem;">Scenario Profiles</h3>
        <p style="font-size: 0.82rem; color: #64748b; margin: 0;">Load pre-calibrated smart grid telemetry profiles:</p>
    </div>
    """, unsafe_allow_html=True)
    
    preset_choice = st.selectbox(
        "Select Electrical Preset",
        options=list(energy_engine.PRESETS.keys()),
        format_func=lambda k: energy_engine.PRESETS[k]["name"],
        index=4,
        label_visibility="collapsed"
    )
    
    preset_data = energy_engine.PRESETS[preset_choice]["data"]
    preset_desc = energy_engine.PRESETS[preset_choice]["description"]
    
    st.markdown(f"""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 14px; margin: 8px 0 16px 0;">
        <div style="font-size: 0.8rem; color: #334155; line-height: 1.45;">{preset_desc}</div>
        <div style="margin-top: 8px; display: flex; gap: 6px; flex-wrap: wrap;">
            <span class="badge-mono badge-mono-slate">V: {preset_data.get('Voltage', 230)}V</span>
            <span class="badge-mono badge-mono-slate">I: {preset_data.get('Global_intensity', 10)}A</span>
            <span class="badge-mono badge-mono-slate">Sub3: {preset_data.get('Sub_metering_3', 0)}Wh</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div>
        <h4 style="margin: 0 0 4px 0; font-size: 1.05rem;"><i class="fa-regular fa-clock"></i> Temporal Synchronization</h4>
        <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 10px;">Derive hour, weekday, and tariff peaks dynamically:</p>
    </div>
    """, unsafe_allow_html=True)
    
    use_current_dt = st.checkbox("Auto-derive from local clock", value=True)
    
    if use_current_dt:
        dt_current = datetime.now()
        derived_time = energy_engine.derive_time_features(dt_current)
        st.markdown(f"""
        <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 12px; margin-top: 8px;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #1e40af;">
                <strong>SYNCED TIME:</strong> {dt_current.strftime('%H:%M:%S')}<br>
                <strong>TARIFF:</strong> {'⚡ Peak (6-10 PM)' if derived_time['Peak_Hour'] == 1 else '🌱 Off-Peak Window'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        selected_date = st.date_input("Select Date", datetime.now().date())
        selected_hour = st.slider("Hour of Day (0-23)", 0, 23, 18)
        dt_custom = datetime.combine(selected_date, datetime.min.time()).replace(hour=selected_hour)
        derived_time = energy_engine.derive_time_features(dt_custom)
        st.markdown(f"""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; margin-top: 8px;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #334155;">
                <strong>HOUR:</strong> {derived_time['Hour']}:00 | <strong>PEAK:</strong> {'YES' if derived_time['Peak_Hour'] == 1 else 'NO'}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 1. Interactive Generative Electric Wave Hero Banner (HTML5 Canvas Component)
# ==============================================================================
current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hero_canvas_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=JetBrains+Mono:wght@600;700;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
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
            padding: 22px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            pointer-events: none;
            background: linear-gradient(90deg, rgba(9,13,22,0.92) 0%, rgba(9,13,22,0.45) 55%, rgba(9,13,22,0.92) 100%);
            min-height: 180px;
        }}
        @media (max-width: 768px) {{
            .hero-overlay {{
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
                padding: 16px;
            }}
        }}
        .hero-left h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.95rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.03em;
            text-shadow: 0 0 24px rgba(0, 242, 254, 0.4);
            margin-bottom: 4px;
        }}
        .hero-left p {{
            font-size: 0.88rem;
            color: #cbd5e1;
            max-width: 620px;
            line-height: 1.45;
        }}
        .badge {{
            display: inline-block;
            background: rgba(0, 242, 254, 0.12);
            border: 1px solid rgba(0, 242, 254, 0.4);
            color: #00f2fe;
            padding: 3px 10px;
            border-radius: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 700;
            margin-bottom: 6px;
            letter-spacing: 0.05em;
        }}
        .hero-right {{
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(0, 242, 254, 0.3);
            border-radius: 10px;
            padding: 12px 18px;
            text-align: right;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}
        .clock-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 700;
            color: #00f2fe;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }}
        .clock-val {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.05rem;
            font-weight: 700;
            color: #ffffff;
            margin-top: 2px;
            letter-spacing: 0.02em;
        }}
        .clock-sub {{
            font-size: 0.68rem;
            color: #94a3b8;
            margin-top: 2px;
        }}
        .wave-hint {{
            position: absolute;
            bottom: 8px;
            left: 30px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            color: rgba(203, 213, 225, 0.6);
            z-index: 2;
            pointer-events: none;
            display: flex;
            align-items: center;
            gap: 6px;
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
            <span class="clock-label"><i class="fa-solid fa-bolt"></i> LOCAL GRID TIME</span>
            <div class="clock-val">{current_time_str}</div>
            <div class="clock-sub">Auto-Sync ML Context (Hour {derived_time['Hour']})</div>
        </div>
    </div>
    <div class="wave-hint"><i class="fa-solid fa-arrow-pointer"></i> Move cursor across canvas to modulate grid waveform physics</div>

    <script>
        const canvas = document.getElementById('waveCanvas');
        const ctx = canvas.getContext('2d');
        
        function resize() {{
            canvas.width = window.innerWidth;
            canvas.height = 180;
        }}
        resize();
        window.addEventListener('resize', resize);

        let mouse = {{ x: canvas.width / 2, y: 90, targetX: canvas.width / 2, targetY: 90 }};
        let time = 0;

        const waves = [
            {{ amplitude: 32, frequency: 0.008, speed: 0.025, color: 'rgba(56, 189, 248, 0.5)', lineWidth: 2.5, phase: 0 }},
            {{ amplitude: 24, frequency: 0.012, speed: 0.035, color: 'rgba(0, 242, 254, 0.65)', lineWidth: 2.0, phase: 2 }},
            {{ amplitude: 38, frequency: 0.006, speed: 0.018, color: 'rgba(16, 185, 129, 0.45)', lineWidth: 2.0, phase: 4 }},
            {{ amplitude: 18, frequency: 0.016, speed: 0.03, color: 'rgba(99, 102, 241, 0.35)', lineWidth: 1.5, phase: 1 }}
        ];

        let particles = [];
        for (let i = 0; i < 40; i++) {{
            particles.push({{
                x: Math.random() * canvas.width,
                y: Math.random() * 180,
                radius: Math.random() * 2 + 1,
                vx: (Math.random() - 0.5) * 0.8,
                vy: (Math.random() - 0.5) * 0.8,
                alpha: Math.random() * 0.7 + 0.3,
                color: Math.random() > 0.35 ? '#00f2fe' : '#10b981'
            }});
        }}

        window.addEventListener('mousemove', (e) => {{
            const rect = canvas.getBoundingClientRect();
            mouse.targetX = e.clientX - rect.left;
            mouse.targetY = e.clientY - rect.top;
        }});

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            time += 1;
            mouse.x += (mouse.targetX - mouse.x) * 0.06;
            mouse.y += (mouse.targetY - mouse.y) * 0.06;

            waves.forEach((w, idx) => {{
                ctx.beginPath();
                ctx.lineWidth = w.lineWidth;
                ctx.strokeStyle = w.color;
                ctx.shadowColor = w.color;
                ctx.shadowBlur = 8;

                const baseH = canvas.height * 0.5 + (idx - 1.5) * 14;
                for (let x = 0; x <= canvas.width; x += 5) {{
                    const dx = x - mouse.x;
                    const dy = baseH - mouse.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    const influence = Math.max(0, 1 - dist / 180) * 32;

                    const y = baseH + Math.sin(x * w.frequency + time * w.speed + w.phase) * w.amplitude - influence * Math.sin(time * 0.05);
                    if (x === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }}
                ctx.stroke();
                ctx.shadowBlur = 0;
            }});

            particles.forEach(p => {{
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0) p.x = canvas.width; if (p.x > canvas.width) p.x = 0;
                if (p.y < 0) p.y = 180; if (p.y > 180) p.y = 0;

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
                    if (dist < 75) {{
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(0, 242, 254, ${{0.22 * (1 - dist / 75)}})`;
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

# ==============================================================================
# Navigation Tabs
# ==============================================================================
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
    st.markdown("""
    <div style="margin: 6px 0 16px 0;">
        <span class="badge-mono badge-mono-blue"><i class="fa-solid fa-diagram-project"></i> PIPELINE ARCHITECTURE</span>
        <h3 style="margin: 6px 0 4px 0; font-size: 1.4rem;">How the Smart Grid Demand Forecasting Pipeline Works</h3>
        <p style="color: #475569; font-size: 0.92rem; margin: 0;">
            A structured machine learning system that transforms high-frequency smart meter readings into actionable load balancing and cost projections.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Connected Pipeline Sequence
    st.markdown("""
    <div class="pipeline-container">
        <div class="pipeline-step">
            <span class="pipeline-badge">STAGE 01</span>
            <h4>Telemetry Ingestion</h4>
            <p>Captures 15 simultaneous inputs including voltage, current, sub-metering, and rolling averages.</p>
        </div>
        <div class="pipeline-step">
            <span class="pipeline-badge">STAGE 02</span>
            <h4>PCA Compression</h4>
            <p>Reduces 15 correlated dimensions into 12 orthogonal components, preserving &gt;95% data variance.</p>
        </div>
        <div class="pipeline-step">
            <span class="pipeline-badge">STAGE 03</span>
            <h4>Linear Regression</h4>
            <p>Fits transformed vectors to produce high-throughput active power demand forecasts in kW.</p>
        </div>
        <div class="pipeline-step">
            <span class="pipeline-badge">STAGE 04</span>
            <h4>Load Optimization</h4>
            <p>Translates kW output into financial billing estimates, CO₂ emissions, and peak shaving advice.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin: 20px 0 12px 0;">
        <span class="badge-mono badge-mono-slate"><i class="fa-solid fa-layer-group"></i> RESIDENTIAL LOAD ZONES</span>
        <h4 style="margin: 6px 0 4px 0; font-size: 1.2rem;">Sub-Metering Classification</h4>
    </div>
    """, unsafe_allow_html=True)
    
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    
    with sub_col1:
        st.markdown("""
        <div class="neutral-card">
            <div class="card-header-mono" style="color: #2563eb;">
                <i class="fa-solid fa-utensils"></i> SUB-METERING 1
            </div>
            <div class="card-title-jakarta" style="font-size: 1.05rem; margin-bottom: 8px;">Kitchen Zone</div>
            <p style="font-size: 0.86rem; color: #475569; margin-bottom: 10px; line-height: 1.45;">
                <strong>Appliances:</strong> Dishwasher, microwave, oven, kitchen auxiliaries.
            </p>
            <p style="font-size: 0.84rem; color: #64748b; margin: 0; line-height: 1.4;">
                <em>Pattern:</em> Pronounced morning and dinner spike windows with high instantaneous current.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with sub_col2:
        st.markdown("""
        <div class="neutral-card">
            <div class="card-header-mono" style="color: #7c3aed;">
                <i class="fa-solid fa-shirt"></i> SUB-METERING 2
            </div>
            <div class="card-title-jakarta" style="font-size: 1.05rem; margin-bottom: 8px;">Laundry Zone</div>
            <p style="font-size: 0.86rem; color: #475569; margin-bottom: 10px; line-height: 1.45;">
                <strong>Appliances:</strong> Washing machine, tumble dryer, laundry heating.
            </p>
            <p style="font-size: 0.84rem; color: #64748b; margin: 0; line-height: 1.4;">
                <em>Pattern:</em> Concentrated weekend and daytime cycles. Prime target for off-peak shifting.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with sub_col3:
        st.markdown("""
        <div class="neutral-card">
            <div class="card-header-mono" style="color: #d97706;">
                <i class="fa-solid fa-temperature-arrow-up"></i> SUB-METERING 3
            </div>
            <div class="card-title-jakarta" style="font-size: 1.05rem; margin-bottom: 8px;">Climate & Heating</div>
            <p style="font-size: 0.86rem; color: #475569; margin-bottom: 10px; line-height: 1.45;">
                <strong>Appliances:</strong> Air conditioning, electric water heater, space heating.
            </p>
            <p style="font-size: 0.84rem; color: #64748b; margin: 0; line-height: 1.4;">
                <em>Pattern:</em> Heavy continuous draw during extreme weather and evening peak hours (6 to 10 PM).
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 1: Interactive Circuit Board Component
# ==============================================================================
with tab_circuit:
    st.markdown("""
    <div style="margin: 6px 0 14px 0;">
        <span class="badge-mono badge-mono-blue"><i class="fa-solid fa-network-wired"></i> REAL-TIME FLOW</span>
        <h3 style="margin: 6px 0 4px 0; font-size: 1.4rem;">Interactive Household Circuit & Energy Flow Map</h3>
        <p style="color: #475569; font-size: 0.9rem; margin: 0;">
            Live electron current simulation from the grid substation through the smart IoT meter into sub-metered appliance branches.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    circuit_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&family=JetBrains+Mono:wght@600;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
            body { 
                background: #0f172a; 
                color: #ffffff; 
                padding: 24px; 
                border-radius: 14px;
                border: 1px solid rgba(0, 242, 254, 0.2);
            }
            .board { 
                display: flex; 
                align-items: center; 
                justify-content: space-between; 
                gap: 20px; 
            }
            @media (max-width: 800px) {
                .board {
                    flex-direction: column;
                    gap: 16px;
                }
                .wire {
                    width: 3px !important;
                    height: 28px !important;
                }
                .pulse {
                    animation: flow-v 1.5s linear infinite !important;
                }
                @keyframes flow-v {
                    0% { top: -10%; opacity: 0; left: -4px; }
                    20% { opacity: 1; }
                    80% { opacity: 1; }
                    100% { top: 110%; opacity: 0; left: -4px; }
                }
            }
            .node {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(0,242,254,0.3);
                border-radius: 12px;
                padding: 18px 22px;
                text-align: center;
                min-width: 170px;
                transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
            }
            .node:hover { 
                transform: translateY(-3px); 
                border-color: #00f2fe; 
                box-shadow: 0 0 20px rgba(0,242,254,0.35); 
            }
            .node i { font-size: 26px; color: #00f2fe; margin-bottom: 8px; }
            .node strong { 
                display: block; 
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 0.96rem; 
                color: #ffffff;
            }
            .node small { 
                font-family: 'JetBrains Mono', monospace; 
                font-size: 0.75rem; 
                color: #94a3b8; 
            }
            .wire { 
                flex: 1; 
                height: 3px; 
                background: rgba(255,255,255,0.15); 
                position: relative; 
                overflow: hidden; 
            }
            .pulse { 
                position: absolute; 
                top: -4px; 
                width: 12px; 
                height: 12px; 
                border-radius: 50%; 
                background: #00f2fe; 
                box-shadow: 0 0 12px #00f2fe; 
                animation: flow 2s linear infinite; 
            }
            .pulse.delay { animation-delay: 1s; }
            @keyframes flow { 
                0% { left: -10%; opacity: 0; } 
                20% { opacity: 1; } 
                80% { opacity: 1; } 
                100% { left: 110%; opacity: 0; } 
            }
            .branches { 
                display: flex; 
                flex-direction: column; 
                gap: 10px; 
                min-width: 220px; 
            }
            .app-card { 
                background: rgba(255,255,255,0.05); 
                border: 1px solid rgba(255,255,255,0.1); 
                border-radius: 8px; 
                padding: 10px 14px; 
                display: flex; 
                align-items: center; 
                gap: 12px; 
                transition: transform 0.15s, border-color 0.15s;
            }
            .app-card:hover {
                transform: translateX(4px);
                border-color: rgba(0, 242, 254, 0.4);
            }
            .app-card i { color: #00f2fe; font-size: 16px; width: 20px; text-align: center; }
            .app-card strong { font-size: 0.84rem; color: #f1f5f9; }
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
    components.html(circuit_html, height=210, scrolling=False)

# ==============================================================================
# TAB 2: Demand Predictor Workspace
# ==============================================================================
with tab_predict:
    st.markdown("""
    <div style="margin: 6px 0 16px 0;">
        <span class="badge-mono badge-mono-blue"><i class="fa-solid fa-sliders"></i> ML INFERENCE WORKBENCH</span>
        <h3 style="margin: 6px 0 4px 0; font-size: 1.4rem;">Input Telemetry & Environmental Readings</h3>
        <p style="color: #475569; font-size: 0.9rem; margin: 0;">
            Calibrate raw sensor readings, instantaneous sub-metered watt-hours, and historical rolling power context.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        st.markdown("""
        <div class="neutral-card" style="margin-bottom: 12px; padding: 18px 20px;">
            <div class="card-header-mono"><i class="fa-solid fa-bolt"></i> TELEMETRY INPUTS</div>
            <div class="card-title-jakarta" style="font-size: 1.05rem;">Electrical Telemetry</div>
        </div>
        """, unsafe_allow_html=True)
        Voltage = st.number_input("Supply Voltage (V)", value=float(preset_data.get("Voltage", 234.84)), step=0.5, format="%.2f")
        Global_intensity = st.number_input("Current Intensity (A)", value=float(preset_data.get("Global_intensity", 18.4)), step=0.1, format="%.2f")
        Global_reactive_power = st.number_input("Global Reactive Power (kVAR)", value=float(preset_data.get("Global_reactive_power", 0.418)), step=0.01, format="%.3f")
        
    with col_e2:
        st.markdown("""
        <div class="neutral-card" style="margin-bottom: 12px; padding: 18px 20px;">
            <div class="card-header-mono"><i class="fa-solid fa-plug"></i> ZONE CONSUMPTION</div>
            <div class="card-title-jakarta" style="font-size: 1.05rem;">Sub-Metering Loads (Wh)</div>
        </div>
        """, unsafe_allow_html=True)
        Sub_metering_1 = st.number_input("Sub 1: Kitchen (Wh)", value=float(preset_data.get("Sub_metering_1", 0.0)), step=1.0, format="%.1f")
        Sub_metering_2 = st.number_input("Sub 2: Laundry (Wh)", value=float(preset_data.get("Sub_metering_2", 1.0)), step=1.0, format="%.1f")
        Sub_metering_3 = st.number_input("Sub 3: HVAC / Boiler (Wh)", value=float(preset_data.get("Sub_metering_3", 17.0)), step=1.0, format="%.1f")
        
    with col_e3:
        st.markdown("""
        <div class="neutral-card" style="margin-bottom: 12px; padding: 18px 20px;">
            <div class="card-header-mono"><i class="fa-regular fa-clock"></i> HISTORICAL & TEMPORAL</div>
            <div class="card-title-jakarta" style="font-size: 1.05rem;">Baseline & Context</div>
        </div>
        """, unsafe_allow_html=True)
        Previous_Power = st.number_input("Previous Minute Power (kW)", value=float(preset_data.get("Previous_Power", 4.216)), step=0.1, format="%.3f")
        Rolling_Mean_24 = st.number_input("24h Rolling Mean Power (kW)", value=float(preset_data.get("Rolling_Mean_24", 1.091)), step=0.1, format="%.3f")
        
        st.markdown(f"""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; margin-top: 12px;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #475569; line-height: 1.6;">
                <div>Hour: <strong>{derived_time['Hour']}</strong> | Day: <strong>{derived_time['Day']}</strong> | Mo: <strong>{derived_time['Month']}</strong></div>
                <div>Weekend: <strong>{'Yes' if derived_time['Weekend'] == 1 else 'No'}</strong> | Peak (6-10PM): <strong>{'Yes' if derived_time['Peak_Hour'] == 1 else 'No'}</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
    
    st.markdown("<hr style='margin: 24px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="margin: 0 0 16px 0;">
        <span class="badge-mono badge-mono-blue"><i class="fa-solid fa-chart-line"></i> PREDICTIVE ANALYTICS</span>
        <h3 style="margin: 6px 0 4px 0; font-size: 1.4rem;">Demand Forecasting Results & Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    res_col_left, res_col_right = st.columns([1.2, 2])
    
    with res_col_left:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pred_kw,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "<b>Predicted Active Demand</b>", 'font': {'size': 15, 'color': '#0f172a', 'family': 'Plus Jakarta Sans'}},
            number={'suffix': " kW", 'font': {'size': 32, 'color': '#2563eb', 'family': 'JetBrains Mono'}},
            gauge={
                'axis': {'range': [0, 6], 'tickwidth': 1, 'tickcolor': "#64748b", 'tickfont': {'family': 'JetBrains Mono', 'size': 11}},
                'bar': {'color': analytics["tier_color"], 'thickness': 0.28},
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
            margin=dict(l=20, r=20, t=40, b=10),
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with res_col_right:
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric(
                label="Efficiency Tier",
                value=analytics["tier"],
                delta="Off-Peak Window" if derived_time["Peak_Hour"] == 0 else "Peak Tariff Period",
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

        tier_class = "danger" if "Peak" in analytics["tier"] or "High" in analytics["tier"] else ("warn" if "Moderate" in analytics["tier"] else "")
        st.markdown(f"""
        <div class="tip-box-neutral {tier_class}">
            <strong><i class="fa-solid fa-lightbulb"></i> Grid Advisory:</strong> {analytics['tier_advice']}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        st.markdown("""
        <div style="margin-bottom: 8px;">
            <h4 style="margin: 0; font-size: 1.1rem;"><i class="fa-solid fa-chart-pie"></i> Appliance Sub-Metering Breakdown</h4>
        </div>
        """, unsafe_allow_html=True)
        bd = analytics["breakdown"]
        labels = ['Kitchen (Sub 1)', 'Laundry (Sub 2)', 'HVAC / Heating (Sub 3)', 'Baseline Load']
        values = [bd['kitchen_pct'], bd['laundry_pct'], bd['hvac_pct'], bd['base_pct']]
        colors = ['#2563eb', '#7c3aed', '#d97706', '#059669']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.6,
            marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
            textinfo='percent',
            textfont=dict(family="JetBrains Mono", size=12)
        )])
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(font=dict(family="Inter", color="#475569", size=11), orientation="h", y=-0.12)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with c_col2:
        st.markdown("""
        <div style="margin-bottom: 8px;">
            <h4 style="margin: 0; font-size: 1.1rem;"><i class="fa-solid fa-chart-area"></i> Simulated 24-Hour Load Profile</h4>
        </div>
        """, unsafe_allow_html=True)
        hours = list(range(24))
        fig_line = px.area(
            x=hours,
            y=analytics["simulated_24h"],
            labels={'x': 'Hour of Day (0-23)', 'y': 'Demand (kW)'},
        )
        fig_line.update_traces(line_color='#2563eb', fillcolor='rgba(37, 99, 235, 0.12)')
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(family="Inter"),
            xaxis=dict(gridcolor="#f1f5f9", tickfont=dict(family="JetBrains Mono", size=10), color="#64748b"),
            yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(family="JetBrains Mono", size=10), color="#64748b")
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ==============================================================================
# TAB 3: Load Simulator & What-If Optimizer
# ==============================================================================
with tab_simulator:
    st.markdown("""
    <div style="margin: 6px 0 16px 0;">
        <span class="badge-mono badge-mono-blue"><i class="fa-solid fa-calculator"></i> WHAT-IF EXPERIMENTATION</span>
        <h3 style="margin: 6px 0 4px 0; font-size: 1.4rem;">Interactive 'What-If' Energy Simulator</h3>
        <p style="color: #475569; font-size: 0.9rem; margin: 0;">
            Simulate the demand, tariff, and carbon reduction impact of adjusting high-draw appliances or rescheduling cycles into off-peak windows.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    sim_col1, sim_col2 = st.columns([1, 1.2])
    
    with sim_col1:
        st.markdown("""
        <div class="neutral-card">
            <div class="card-header-mono"><i class="fa-solid fa-sliders"></i> SIMULATION CONTROLS</div>
            <div class="card-title-jakarta" style="font-size: 1.05rem; margin-bottom: 14px;">Appliance Overrides</div>
        """, unsafe_allow_html=True)
        hvac_toggle = st.slider("HVAC / Water Heater Load (Wh)", 0.0, 40.0, float(Sub_metering_3), step=1.0)
        laundry_toggle = st.slider("Laundry Load (Wh)", 0.0, 40.0, float(Sub_metering_2), step=1.0)
        shift_off_peak = st.checkbox("Reschedule load to Off-Peak Hour (2:00 PM)", value=False)
        st.markdown("</div>", unsafe_allow_html=True)
        
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
        
        st.markdown("""
        <div class="neutral-card">
            <div class="card-header-mono"><i class="fa-solid fa-chart-column"></i> PREDICTED IMPACT</div>
            <div class="card-title-jakarta" style="font-size: 1.05rem; margin-bottom: 14px;">Simulated Impact vs Baseline</div>
        """, unsafe_allow_html=True)
        
        sm_col1, sm_col2 = st.columns(2)
        with sm_col1:
            st.metric(
                label="Simulated Active Demand",
                value=f"{sim_kw:.3f} kW",
                delta=f"{delta_kw:+.3f} kW",
                delta_color="inverse"
            )
        with sm_col2:
            st.metric(
                label="Projected Monthly Bill Delta",
                value=f"${sim_result['monthly_cost_usd']:.2f}",
                delta=f"${delta_cost_mo:+.2f} / month",
                delta_color="inverse"
            )
            
        if delta_kw < -0.05:
            co2_saved = abs(delta_kw) * 24 * 30.5 * 0.475
            st.markdown(f"""
            <div class="tip-box-neutral" style="margin-top: 12px;">
                <strong><i class="fa-solid fa-leaf" style="color: #059669;"></i> Eco-Optimization:</strong> 
                This rescheduled load profile reduces carbon emissions by approximately <strong>{co2_saved:.1f} kg CO₂</strong> per month and cuts electricity expenditure by <strong>${abs(delta_cost_mo):.2f}/mo</strong>.
            </div>
            """, unsafe_allow_html=True)
        elif delta_kw > 0.05:
            st.markdown(f"""
            <div class="tip-box-neutral warn" style="margin-top: 12px;">
                <strong><i class="fa-solid fa-triangle-exclamation" style="color: #d97706;"></i> Increased Load:</strong> 
                The simulated changes increase demand by <strong>+{delta_kw:.3f} kW</strong>. Consider shifting high-power cycles away from peak grid hours.
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # Overlaid 24-Hour Before / After Comparison Chart
    st.markdown("""
    <div style="margin: 18px 0 8px 0;">
        <span class="badge-mono badge-mono-slate"><i class="fa-solid fa-code-compare"></i> 24-HOUR OPTIMIZATION CURVE</span>
        <h4 style="margin: 6px 0 4px 0; font-size: 1.15rem;">Baseline vs. Simulated 24-Hour Load Profiles</h4>
    </div>
    """, unsafe_allow_html=True)
    
    hours = list(range(24))
    baseline_24h = analytics["simulated_24h"]
    simulated_24h = sim_result["simulated_24h"]
    
    fig_compare = go.Figure()
    
    # Baseline Area / Line
    fig_compare.add_trace(go.Scatter(
        x=hours,
        y=baseline_24h,
        mode='lines',
        name='Baseline Profile',
        line=dict(color='#2563eb', width=2.5, dash='dot'),
        fill='tozeroy',
        fillcolor='rgba(37, 99, 235, 0.08)'
    ))
    
    # Simulated Area / Line
    fig_compare.add_trace(go.Scatter(
        x=hours,
        y=simulated_24h,
        mode='lines',
        name='Simulated Profile',
        line=dict(color='#059669', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(5, 150, 105, 0.12)'
    ))
    
    fig_compare.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        font=dict(family="Inter"),
        legend=dict(
            font=dict(family="Inter", size=12),
            orientation="h",
            y=1.1,
            x=0
        ),
        xaxis=dict(
            title="Hour of Day (0-23)",
            gridcolor="#f1f5f9",
            tickfont=dict(family="JetBrains Mono", size=10),
            color="#64748b"
        ),
        yaxis=dict(
            title="Predicted Demand (kW)",
            gridcolor="#f1f5f9",
            tickfont=dict(family="JetBrains Mono", size=10),
            color="#64748b"
        )
    )
    st.plotly_chart(fig_compare, use_container_width=True)

# ==============================================================================
# TAB 4: ML & PCA Architecture
# ==============================================================================
with tab_analytics:
    st.markdown("""
    <div style="margin: 6px 0 16px 0;">
        <span class="badge-mono badge-mono-blue"><i class="fa-solid fa-brain"></i> MODEL INTERNALS</span>
        <h3 style="margin: 6px 0 4px 0; font-size: 1.4rem;">Model Diagnostics & Dimensionality Analysis</h3>
        <p style="color: #475569; font-size: 0.9rem; margin: 0;">
            Mathematical transparency of the ML training pipeline, standardization transformations, and principal component variance retention.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    arch_col1, arch_col2 = st.columns([1, 1.3])
    with arch_col1:
        st.markdown("""
        <div class="neutral-card">
            <div class="card-header-mono"><i class="fa-solid fa-list-check"></i> PIPELINE STAGES</div>
            <div class="card-title-jakarta" style="font-size: 1.1rem; margin-bottom: 12px;">Machine Learning Pipeline</div>
            <div style="font-size: 0.86rem; color: #334155; line-height: 1.6;">
                <div style="margin-bottom: 10px;">
                    <strong style="color: #0f172a;">1. SimpleImputer:</strong><br>
                    Imputes missing telemetry values using median statistics computed across historic grid cycles.
                </div>
                <div style="margin-bottom: 10px;">
                    <strong style="color: #0f172a;">2. StandardScaler:</strong><br>
                    Normalizes 15 raw feature distributions to zero mean & unit variance ($\mu=0, \sigma=1$).
                </div>
                <div style="margin-bottom: 10px;">
                    <strong style="color: #0f172a;">3. PCA (Principal Component Analysis):</strong><br>
                    Compresses <strong>15 correlated dimensions</strong> down to <strong>12 orthogonal components</strong>, preserving &gt;95% variance and eliminating collinearity between current, voltage, and sub-metering.
                </div>
                <div>
                    <strong style="color: #0f172a;">4. Linear Regression:</strong><br>
                    High-throughput, explainable model predicting continuous active power output in kilowatts (kW).
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with arch_col2:
        pca_obj = energy_engine.pca
        var_ratios = pca_obj.explained_variance_ratio_
        cum_var = np.cumsum(var_ratios)
        pc_names = [f"PC{i+1}" for i in range(len(var_ratios))]
        
        # Cumulative Variance Plot
        fig_pca = go.Figure()
        
        # Bar for individual variance
        fig_pca.add_trace(go.Bar(
            x=pc_names,
            y=var_ratios * 100,
            name='Individual Variance (%)',
            marker_color='rgba(37, 99, 235, 0.7)',
            yaxis='y'
        ))
        
        # Line for cumulative variance
        fig_pca.add_trace(go.Scatter(
            x=pc_names,
            y=cum_var * 100,
            name='Cumulative Variance (%)',
            mode='lines+markers',
            line=dict(color='#059669', width=2.5),
            marker=dict(size=6, color='#059669'),
            yaxis='y'
        ))
        
        # 95% Threshold Line
        fig_pca.add_shape(
            type='line',
            x0=pc_names[0],
            x1=pc_names[-1],
            y0=95,
            y1=95,
            line=dict(color='#dc2626', width=1.5, dash='dash')
        )
        
        fig_pca.add_annotation(
            x=pc_names[-2],
            y=97,
            text=">95% Variance Threshold",
            showarrow=False,
            font=dict(family="JetBrains Mono", size=10, color="#dc2626")
        )
        
        fig_pca.update_layout(
            title=dict(text="<b>PCA Explained & Cumulative Variance Ratio</b>", font=dict(family="Plus Jakarta Sans", size=14, color="#0f172a")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=260,
            margin=dict(l=10, r=10, t=40, b=10),
            font=dict(family="Inter"),
            legend=dict(font=dict(family="Inter", size=11), orientation="h", y=-0.2),
            xaxis=dict(gridcolor="#f1f5f9", tickfont=dict(family="JetBrains Mono", size=10), color="#64748b"),
            yaxis=dict(title="Variance (%)", range=[0, 105], gridcolor="#f1f5f9", tickfont=dict(family="JetBrains Mono", size=10), color="#64748b")
        )
        
        st.plotly_chart(fig_pca, use_container_width=True)

    st.markdown("""
    <div style="margin: 16px 0 8px 0;">
        <span class="badge-mono badge-mono-slate"><i class="fa-solid fa-table"></i> EIGENVALUE DATA MATRIX</span>
        <h4 style="margin: 6px 0 4px 0; font-size: 1.15rem;">PCA Components Variance Summary</h4>
    </div>
    """, unsafe_allow_html=True)
    
    df_pca = pd.DataFrame({
        "Component": [f"PC {i+1}" for i in range(len(var_ratios))],
        "Explained Variance Ratio": var_ratios,
        "Cumulative Variance": cum_var
    })
    st.dataframe(df_pca.style.format({
        "Explained Variance Ratio": "{:.2%}",
        "Cumulative Variance": "{:.2%}"
    }), use_container_width=True)