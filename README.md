# ⚡ VoltIQ — Smart Grid Energy Management & Real-Time Demand Forecasting

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5%2B-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

> **VoltIQ** is an end-to-end, data-driven smart grid energy management and load forecasting system. It analyzes high-frequency electrical telemetry and temporal parameters, applies machine learning and Principal Component Analysis (PCA) to forecast active power consumption, decomposes residential sub-metering zones, and provides actionable load-balancing, billing, and carbon footprint insights via both an interactive **Streamlit Analytics Platform** and a **Production Flask Web Application with REST API**.

---

## 🌟 Key Highlights & Capabilities

- 🔬 **Robust Machine Learning Pipeline**: Vector-accelerated inference with automated missing-value imputation, standard feature scaling, 12-component PCA compression (preserving $>95\%$ variance), and linear demand regression.
- ⚡ **Real-Time Active Power Forecasting**: High-throughput prediction of global active power consumption ($kW$) with instant demand classification into **Eco Low**, **Nominal Usage**, and **High Peak Alert** tiers.
- 🔌 **Granular Sub-Metering Decomposition**: Decomposes power usage across residential zones:
  - **Sub-Metering 1**: Kitchen & cooking auxiliaries (microwave, dishwasher, oven)
  - **Sub-Metering 2**: Laundry room (washing machine, dryer, refrigeration)
  - **Sub-Metering 3**: Climate control & water heating (HVAC, AC units, boiler)
  - **Base Load**: Residual lighting, background standby, and entertainment
- 💰 **Dual-Currency Billing & Peak Tariff Modeling**: Computes instantaneous hourly and monthly billing projections in both USD ($) and INR (₹), integrating dynamic Time-of-Use (ToU) peak tariff detection (6:00 PM – 10:00 PM).
- 🌱 **Carbon Footprint Monitoring**: Calculates continuous greenhouse gas emissions ($0.475\text{ kg CO}_2/\text{kWh}$) to encourage peak shaving and sustainability.
- 🔮 **24-Hour Load Curve Simulation**: Dynamically models circadian consumption patterns and what-if load-shifting scenarios.
- 🎨 **State-of-the-Art Visual Aesthetics**: Generative HTML5 interactive electric wave canvas hero header, glassmorphic instrument cards, 3D interactive physics simulation, and Plotly financial analytics.
- 🚀 **Dual Deployment Architecture**:
  - **Streamlit Platform**: Feature-rich dashboard for energy engineers, data scientists, and grid operators.
  - **Flask Web Server & REST API**: Production-ready microservice with REST endpoints for smart meter IoT ingestion.

---

## 🏗️ System Architecture & Workflow

```mermaid
flowchart TD
    subgraph Ingestion["1. Telemetry Ingestion"]
        A[Smart Meter IoT Telemetry] --> D[15-Feature Input Vector]
        B[Local Clock / User DateTime] --> D
        C[Scenario Presets] --> D
    end

    subgraph Preprocessing["2. Preprocessing & Compression"]
        D --> E[Statistical Imputer\nMedian Baseline Fallback]
        E --> F[Standard Scaler\nZero Mean & Unit Variance]
        F --> G[PCA Transformer\n15 Features → 12 Orthogonal Components]
    end

    subgraph Inference["3. Demand Inference"]
        G --> H[Linear Regression Model\nActive Power Prediction (kW)]
    end

    subgraph Analytics["4. Derived Energy Analytics"]
        H --> I1[Tier Classification\nEco / Nominal / Peak Alert]
        H --> I2[Sub-Metering Wattage Decomposition\nKitchen / Laundry / HVAC / Base]
        H --> I3[Billing Projections\nHourly & Monthly in USD & INR]
        H --> I4[Carbon Emissions\n0.475 kg CO₂ / kWh]
        H --> I5[24-Hour Circadian Load Curve]
    end

    subgraph Presentation["5. Interfaces & API"]
        I1 & I2 & I3 & I4 & I5 --> J[Streamlit Analytics Platform]
        I1 & I2 & I3 & I4 & I5 --> K[Flask REST API & Dashboard]
    end
```

---

## 🖥️ Streamlit Interactive Workspace Modules

The Streamlit dashboard (`streamlit_app.py`) provides 5 interconnected workspaces:

| Tab Module | Description | Key Features |
| :--- | :--- | :--- |
| **1. System Overview & Working** | End-to-end documentation of the smart grid forecasting lifecycle. | Pipeline stage cards, sub-metering classification schema, formula references. |
| **2. Interactive Circuit Simulation** | Real-time electrical schematic and energy flow visualizer. | Live telemetry animations, voltage/current balance, grid stress indicators. |
| **3. Demand Predictor Workspace** | Core live telemetry testing and diagnostic console. | Telemetry sliders, instant kW gauge, billing & carbon cards, 24h diurnal curve. |
| **4. Load Simulator & What-If** | Stress testing and appliance scheduling simulator. | Appliance addition sandbox, peak tariff window shifting, cost reduction analysis. |
| **5. ML Architecture & PCA** | Deep-dive statistical and model explainability inspector. | PCA scree plot, explained variance ratio, eigenvalue loadings matrix, evaluation metrics. |

---

## 📂 Project Repository Structure

```text
smart-grid-energy-management/
├── app.py                  # Production Flask application & REST API server
├── energy_engine.py        # Core ML inference engine & derived analytics pipeline
├── streamlit_app.py        # Interactive Streamlit analytics & simulation dashboard
├── test_suite.py           # Comprehensive automated test suite (ML, API, Streamlit)
├── requirements.txt        # Python dependency manifest
├── model.pkl               # Serialized linear regression model weights
├── pca.pkl                 # Fitted Principal Component Analysis transformer (12 components)
├── scaler.pkl              # Fitted StandardScaler parameters
├── imputer.pkl             # Fitted SimpleImputer parameters
├── templates/              # Jinja2 HTML templates for Flask
│   ├── landing.html        # Comprehensive architectural landing page
│   ├── index.html          # Secondary landing template
│   └── predict.html        # Interactive prediction & telemetry dashboard
└── static/                 # Frontend assets & styles
    ├── style.css           # Custom design system stylesheet
    ├── energy-waves.js     # Generative HTML5 canvas electric wave physics
    └── main.js             # Client-side form handlers & dynamic REST API client
```

---

## 📊 Feature Dictionary & Telemetry Inputs

The machine learning pipeline consumes a 15-dimensional vector:

| Feature Name | Description | Units | Range / Format |
| :--- | :--- | :--- | :--- |
| `Global_reactive_power` | Total reactive electrical power | $kVAR$ | `0.0 – 1.5` |
| `Voltage` | RMS supply line voltage | $V$ | `220.0 – 260.0` |
| `Global_intensity` | Current intensity draw across all phases | $A$ | `0.2 – 40.0` |
| `Sub_metering_1` | Active energy in Kitchen zone | $Wh$ | `0.0 – 40.0` |
| `Sub_metering_2` | Active energy in Laundry zone | $Wh$ | `0.0 – 40.0` |
| `Sub_metering_3` | Active energy in HVAC / Climate zone | $Wh$ | `0.0 – 40.0` |
| `Hour` | Hour of day | $h$ | `0 – 23` |
| `Day` | Day of the month | $d$ | `1 – 31` |
| `Month` | Calendar month | $m$ | `1 – 12` |
| `Year` | Calendar year | $yr$ | Integer (e.g. `2024`) |
| `Weekday` | Day of week (0=Mon, 6=Sun) | - | `0 – 6` |
| `Weekend` | Binary indicator for Saturday/Sunday | - | `0` or `1` |
| `Peak_Hour` | Binary flag for evening peak window (18:00–22:00) | - | `0` or `1` |
| `Previous_Power` | Lagged active power from previous interval | $kW$ | `0.0 – 10.0` |
| `Rolling_Mean_24` | 24-hour moving average of active power | $kW$ | `0.0 – 8.0` |

---

## ⚡ Pre-Calibrated Scenario Presets

VoltIQ comes with 5 calibrated real-world telemetry presets:

1. **🌙 Eco Night Baseline**: Late-night idle state, minimal standby draw ($0.04 - 0.35\text{ kW}$).
2. **🍳 Morning Breakfast Peak**: Active kitchen appliances, kettle, toaster, microwave ($2.5 - 3.2\text{ kW}$).
3. **🧺 Weekend Laundry & Chores**: High washing machine, spin dryer, and chore activity ($2.8 - 3.4\text{ kW}$).
4. **🔥 Summer Evening Peak & HVAC**: Heavy climate control & water heating during peak grid tariff hours ($4.2 - 5.5\text{ kW}$).
5. **🏡 Balanced Active Household**: Standard active household with entertainment & nominal lighting ($1.8 - 2.2\text{ kW}$).

---

## 🚀 Getting Started & Installation

### 1. Prerequisites
- Python `3.10` or higher installed
- Git installed

### 2. Clone the Repository
```bash
git clone https://github.com/tushitapandey721/smart-grid-energy-management.git
cd smart-grid-energy-management
```

### 3. Create & Activate Virtual Environment
```bash
# On Linux / macOS
python -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🎮 Running the Applications

### Option A: Launch the Streamlit Analytics Platform
```bash
streamlit run streamlit_app.py
```
> Navigate to `http://localhost:8501` in your browser.

### Option B: Launch the Production Flask Web Server
```bash
python app.py
```
> Navigate to `http://localhost:5000` in your browser.
> - **Landing Page**: `http://localhost:5000/`
> - **Predictor Workspace**: `http://localhost:5000/app`

### Option C: Run the Automated Verification Test Suite
```bash
python test_suite.py
```

---

## 🔌 REST API Reference

The Flask application exposes JSON REST endpoints for external smart meter integration and IoT pipelines:

### 1. Execute Demand Prediction
- **Endpoint**: `POST /api/predict`
- **Headers**: `Content-Type: application/json`
- **Request Body Example**:
```json
{
  "Global_reactive_power": 0.234,
  "Voltage": 235.40,
  "Global_intensity": 12.8,
  "Sub_metering_1": 18.0,
  "Sub_metering_2": 1.0,
  "Sub_metering_3": 12.0,
  "Hour": 8,
  "Day": 12,
  "Month": 10,
  "Year": 2024,
  "Weekday": 1,
  "Weekend": 0,
  "Peak_Hour": 0,
  "Previous_Power": 2.850,
  "Rolling_Mean_24": 1.340
}
```

- **Response Example**:
```json
{
  "success": true,
  "data": {
    "predicted_kw": 2.7851,
    "tier": "Nominal Usage",
    "tier_class": "tier-med",
    "tier_color": "#d97706",
    "tier_icon": "fa-bolt",
    "tier_advice": "Usage is within normal residential parameters. Baseline entertainment, lighting, and moderate appliance activity.",
    "hourly_cost_usd": 0.4456,
    "hourly_cost_inr": 22.28,
    "monthly_estimate_kwh": 2038.7,
    "monthly_cost_usd": 326.19,
    "monthly_cost_inr": 16309.58,
    "carbon_kg_hr": 1.323,
    "breakdown": {
      "kitchen_pct": 38.8,
      "laundry_pct": 2.2,
      "hvac_pct": 25.9,
      "base_pct": 33.1,
      "sub1_wh": 18.0,
      "sub2_wh": 1.0,
      "sub3_wh": 12.0,
      "base_wh": 15.42
    },
    "simulated_24h": [0.975, 0.992, 1.012, 1.025, 1.032, 1.021, 2.367, 2.654, 2.891, 3.012, ...]
  }
}
```

#### Example `curl` Command:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"Global_reactive_power": 0.21, "Voltage": 236.5, "Global_intensity": 7.6, "Sub_metering_1": 0.0, "Sub_metering_2": 1.0, "Sub_metering_3": 17.0, "Hour": 18, "Day": 16, "Month": 12, "Year": 2024, "Weekday": 4, "Weekend": 0, "Peak_Hour": 1, "Previous_Power": 1.85, "Rolling_Mean_24": 1.25}'
```

### 2. Fetch Calibrated Presets
- **Endpoint**: `GET /api/presets`
- **Response**: Full JSON catalog of pre-configured scenario presets.

### 3. Fetch Synchronized Time Features
- **Endpoint**: `GET /api/time`
- **Response**: Current server timestamp split into `Hour`, `Day`, `Month`, `Year`, `Weekday`, `Weekend`, and `Peak_Hour`.

---

## 🛠️ Technology Stack

- **Machine Learning & Analytics**: `scikit-learn`, `numpy`, `pandas`, `joblib`
- **Visualization & UI**: `Streamlit`, `Plotly Express / Graph Objects`, `HTML5 Canvas API`, `FontAwesome 6.5`
- **Web Server & Backend API**: `Flask 3.0+`, `Jinja2`, `RESTful JSON API`
- **Design System**: Vanilla CSS with glassmorphism, responsive grid layout, typography from Google Fonts (*Plus Jakarta Sans*, *Inter*, *JetBrains Mono*).

---

## 📜 Dataset & Reference Acknowledgments

This machine learning model was developed and calibrated using the **Individual Household Electric Power Consumption Dataset** from the **UCI Machine Learning Repository**:
- **Source**: [UCI Machine Learning Repository — Individual Household Electric Power Consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)
- **Observations**: 2,075,259 measurements gathered between December 2006 and November 2010 (47 months).
- **Sampling Rate**: 1-minute sampling resolution of electric power consumption and electrical telemetry.

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute for academic and commercial smart grid applications.
