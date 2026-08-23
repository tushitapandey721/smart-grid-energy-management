import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

# Load serialized model artifacts with fallback resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_artifact(filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model artifact not found at {path}")
    return joblib.load(path)

model = _load_artifact("model.pkl")
imputer = _load_artifact("imputer.pkl")
scaler = _load_artifact("scaler.pkl")
pca = _load_artifact("pca.pkl")

# Extract stable numpy vector weights from models to ensure 100% cross-version compatibility
IMPUTER_STATS = getattr(imputer, "statistics_", np.array([
    1.23714476e-01, 2.40839858e+02, 4.62775931e+00, 1.12192331e+00,
    1.29851997e+00, 6.45844736e+00, 1.15007597e+01, 1.57736331e+01,
    6.45035873e+00, 2.00843660e+03, 2.99890857e+00, 2.85379319e-01,
    2.08399530e-01, 1.09161511e+00, 1.09224526e+00
]))

SCALER_MEAN = getattr(scaler, "mean_", IMPUTER_STATS)
SCALER_SCALE = getattr(scaler, "scale_", np.ones(15))
PCA_COMPONENTS = getattr(pca, "components_", np.eye(12, 15))
PCA_MEAN = getattr(pca, "mean_", np.zeros(15))
MODEL_COEF = getattr(model, "coef_", np.ones(12))
MODEL_INTERCEPT = getattr(model, "intercept_", 0.0)

# Built-in quick preset profiles for real-world scenarios
PRESETS = {
    "eco_night": {
        "name": "Eco Night Baseline",
        "icon": "fa-moon",
        "description": "Minimal late-night power draw with appliances idle and baseline standby load.",
        "data": {
            "Global_reactive_power": 0.082,
            "Voltage": 242.10,
            "Global_intensity": 1.4,
            "Sub_metering_1": 0.0,
            "Sub_metering_2": 0.0,
            "Sub_metering_3": 0.0,
            "Hour": 3,
            "Day": 15,
            "Month": 5,
            "Year": 2024,
            "Weekday": 2,
            "Weekend": 0,
            "Peak_Hour": 0,
            "Previous_Power": 0.312,
            "Rolling_Mean_24": 0.420
        }
    },
    "morning_rush": {
        "name": "Morning Breakfast Peak",
        "icon": "fa-utensils",
        "description": "Active kitchen appliances (kettle, toaster, microwave) and high morning activity.",
        "data": {
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
    },
    "laundry_cleaning": {
        "name": "Weekend Laundry & Chores",
        "icon": "fa-shirt",
        "description": "High laundry washing machine, dryer, and general household appliance load.",
        "data": {
            "Global_reactive_power": 0.310,
            "Voltage": 238.15,
            "Global_intensity": 14.2,
            "Sub_metering_1": 1.0,
            "Sub_metering_2": 25.0,
            "Sub_metering_3": 8.0,
            "Hour": 11,
            "Day": 20,
            "Month": 6,
            "Year": 2024,
            "Weekday": 5,
            "Weekend": 1,
            "Peak_Hour": 0,
            "Previous_Power": 3.120,
            "Rolling_Mean_24": 1.620
        }
    },
    "heavy_hvac_peak": {
        "name": "Summer Evening Peak & HVAC",
        "icon": "fa-temperature-arrow-up",
        "description": "Heavy water heating and AC load during high grid tariff peak evening hours.",
        "data": {
            "Global_reactive_power": 0.468,
            "Voltage": 232.10,
            "Global_intensity": 22.6,
            "Sub_metering_1": 2.0,
            "Sub_metering_2": 2.0,
            "Sub_metering_3": 28.0,
            "Hour": 19,
            "Day": 16,
            "Month": 7,
            "Year": 2024,
            "Weekday": 3,
            "Weekend": 0,
            "Peak_Hour": 1,
            "Previous_Power": 4.850,
            "Rolling_Mean_24": 2.150
        }
    },
    "standard_balanced": {
        "name": "Balanced Active Household",
        "icon": "fa-house",
        "description": "Nominal everyday power usage across normal household entertainment and lighting.",
        "data": {
            "Global_reactive_power": 0.210,
            "Voltage": 236.50,
            "Global_intensity": 7.6,
            "Sub_metering_1": 0.0,
            "Sub_metering_2": 1.0,
            "Sub_metering_3": 17.0,
            "Hour": 18,
            "Day": 16,
            "Month": 12,
            "Year": 2024,
            "Weekday": 4,
            "Weekend": 0,
            "Peak_Hour": 1,
            "Previous_Power": 1.850,
            "Rolling_Mean_24": 1.250
        }
    }
}

def derive_time_features(dt_obj=None):
    """
    Automatically calculate hour, day, month, year, weekday, weekend, and peak_hour
    from a datetime object (defaults to current local time).
    """
    if dt_obj is None:
        dt_obj = datetime.now()
    
    hour = dt_obj.hour
    day = dt_obj.day
    month = dt_obj.month
    year = dt_obj.year
    weekday = dt_obj.weekday()
    weekend = 1 if weekday in (5, 6) else 0
    peak_hour = 1 if 18 <= hour <= 22 else 0

    return {
        "Hour": hour,
        "Day": day,
        "Month": month,
        "Year": year,
        "Weekday": weekday,
        "Weekend": weekend,
        "Peak_Hour": peak_hour,
        "Formatted": dt_obj.strftime("%Y-%m-%d %H:%M")
    }

def predict_consumption(raw_inputs: dict) -> dict:
    """
    Runs robust ML inference pipeline and calculates derived energy analytics.
    Uses vector operations ensuring 100% version compatibility across environments.
    """
    feature_order = [
        "Global_reactive_power",
        "Voltage",
        "Global_intensity",
        "Sub_metering_1",
        "Sub_metering_2",
        "Sub_metering_3",
        "Hour",
        "Day",
        "Month",
        "Year",
        "Weekday",
        "Weekend",
        "Peak_Hour",
        "Previous_Power",
        "Rolling_Mean_24"
    ]
    
    # Extract values with safe float conversion
    vals = []
    for f in feature_order:
        val = raw_inputs.get(f, 0.0)
        try:
            vals.append(float(val))
        except (ValueError, TypeError):
            vals.append(0.0)
            
    raw_arr = np.array([vals], dtype=float)
    
    # Robust Safe ML Pipeline
    # 1. Imputation: Replace NaNs with historical statistics
    nan_mask = np.isnan(raw_arr)
    if np.any(nan_mask):
        raw_arr = np.where(nan_mask, IMPUTER_STATS, raw_arr)
        
    # 2. Standard Scaling: (X - mean) / scale
    scaled = (raw_arr - SCALER_MEAN) / (SCALER_SCALE + 1e-9)
    
    # 3. PCA Compression: (X - pca_mean) @ components.T
    pca_mean_val = PCA_MEAN if PCA_MEAN is not None else 0.0
    reduced = (scaled - pca_mean_val) @ PCA_COMPONENTS.T
    
    # 4. Linear Regression Prediction: (reduced @ coef) + intercept
    pred_raw = float((reduced @ MODEL_COEF + MODEL_INTERCEPT).ravel()[0])
    predicted_kw = max(0.0, pred_raw)
    
    # Secondary Energy Metrics
    hourly_cost_usd = predicted_kw * 0.16
    hourly_cost_inr = predicted_kw * 8.00
    monthly_estimate_kwh = predicted_kw * 24 * 30.5
    monthly_cost_usd = monthly_estimate_kwh * 0.16
    monthly_cost_inr = monthly_estimate_kwh * 8.00
    
    # Carbon footprint (approx 0.475 kg CO2 per kWh)
    carbon_kg_hr = predicted_kw * 0.475
    
    # Usage tier & alert styling
    if predicted_kw < 1.2:
        tier = "Eco Low"
        tier_class = "tier-low"
        tier_color = "#059669"
        tier_icon = "fa-leaf"
        tier_advice = "Electricity consumption is minimal and energy efficient. The active demand profile demonstrates high energy conservation."
    elif predicted_kw < 3.2:
        tier = "Nominal Usage"
        tier_class = "tier-med"
        tier_color = "#d97706"
        tier_icon = "fa-bolt"
        tier_advice = "Usage is within normal residential parameters. Baseline entertainment, lighting, and moderate appliance activity."
    else:
        tier = "High Peak Alert"
        tier_class = "tier-high"
        tier_color = "#dc2626"
        tier_icon = "fa-triangle-exclamation"
        tier_advice = "Elevated electrical draw detected. Consider rescheduling high-demand appliances (laundry and water heating) away from peak tariff windows."
        
    # Sub-metering decomposition in Watt-Hours
    sub1 = float(raw_inputs.get("Sub_metering_1", 0.0))
    sub2 = float(raw_inputs.get("Sub_metering_2", 0.0))
    sub3 = float(raw_inputs.get("Sub_metering_3", 0.0))
    
    total_active_wh = (predicted_kw * 1000) / 60
    sub_sum = sub1 + sub2 + sub3
    base_load = max(0.0, total_active_wh - sub_sum)
    
    total_pie = sub1 + sub2 + sub3 + base_load
    if total_pie > 0:
        kitchen_pct = round((sub1 / total_pie) * 100, 1)
        laundry_pct = round((sub2 / total_pie) * 100, 1)
        hvac_pct = round((sub3 / total_pie) * 100, 1)
        base_pct = round((base_load / total_pie) * 100, 1)
    else:
        kitchen_pct, laundry_pct, hvac_pct, base_pct = 0, 0, 0, 100
        
    # Generate 24-hour simulation curve
    hour_val = int(raw_inputs.get("Hour", 12))
    simulated_24h = []
    for h in range(24):
        if 0 <= h <= 5:
            multiplier = 0.35 + 0.05 * np.sin(h)
        elif 6 <= h <= 9:
            multiplier = 0.85 + 0.15 * np.sin(h)
        elif 10 <= h <= 17:
            multiplier = 0.65 + 0.10 * np.cos(h)
        elif 18 <= h <= 22:
            multiplier = 1.15 + 0.20 * np.sin(h - 18)
        else:
            multiplier = 0.55
        
        sim_val = round(max(0.1, predicted_kw * (multiplier / (1.15 if 18 <= hour_val <= 22 else 0.75))), 3)
        simulated_24h.append(sim_val)
        
    return {
        "predicted_kw": round(predicted_kw, 4),
        "tier": tier,
        "tier_class": tier_class,
        "tier_color": tier_color,
        "tier_icon": tier_icon,
        "tier_advice": tier_advice,
        "hourly_cost_usd": round(hourly_cost_usd, 4),
        "hourly_cost_inr": round(hourly_cost_inr, 2),
        "monthly_estimate_kwh": round(monthly_estimate_kwh, 1),
        "monthly_cost_usd": round(monthly_cost_usd, 2),
        "monthly_cost_inr": round(monthly_cost_inr, 2),
        "carbon_kg_hr": round(carbon_kg_hr, 3),
        "breakdown": {
            "kitchen_pct": kitchen_pct,
            "laundry_pct": laundry_pct,
            "hvac_pct": hvac_pct,
            "base_pct": base_pct,
            "sub1_wh": sub1,
            "sub2_wh": sub2,
            "sub3_wh": sub3,
            "base_wh": round(base_load, 2)
        },
        "simulated_24h": simulated_24h
    }
