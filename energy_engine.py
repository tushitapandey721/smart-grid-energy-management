import os
import joblib
import numpy as np
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

# Built-in quick preset profiles for real-world scenarios
PRESETS = {
    "eco_night": {
        "name": "🌙 Eco Night Baseline",
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
        "name": "🍳 Morning Breakfast Peak",
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
        "name": "🧺 Weekend Laundry & Chores",
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
        "name": "❄️ Summer Evening Peak & AC",
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
        "name": "⚡ Balanced Household",
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
    weekday = dt_obj.weekday() # 0 = Monday, 6 = Sunday
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
    Runs full ML pipeline and calculates derived energy analytics.
    Expects input dictionary with the 15 required features.
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
    
    # Extract values with safe float conversion and defaults
    vals = []
    for f in feature_order:
        val = raw_inputs.get(f, 0.0)
        try:
            vals.append(float(val))
        except (ValueError, TypeError):
            vals.append(0.0)
            
    import pandas as pd
    df_features = pd.DataFrame([vals], columns=feature_order)
    
    # ML Pipeline transformation
    imputed = imputer.transform(df_features)
    scaled = scaler.transform(imputed)
    reduced = pca.transform(scaled)
    pred_raw = model.predict(reduced)
    
    predicted_kw = max(0.0, float(pred_raw.ravel()[0]))
    
    # Secondary Energy Metrics
    # Electricity cost estimates ($0.16/kWh global avg, ₹8.0/kWh Indian grid avg)
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
        tier_color = "#10B981" # Emerald Green
        tier_icon = "fa-leaf"
        tier_advice = "Electricity consumption is minimal and energy efficient. Great job maintaining an eco-friendly footprint!"
    elif predicted_kw < 3.2:
        tier = "Moderate / Nominal"
        tier_class = "tier-med"
        tier_color = "#F59E0B" # Amber
        tier_icon = "fa-bolt"
        tier_advice = "Usage is within normal household parameters. Regular daytime active appliance profile."
    else:
        tier = "High / Peak Alert"
        tier_class = "tier-high"
        tier_color = "#EF4444" # Crimson Red
        tier_icon = "fa-fire-flame-curved"
        tier_advice = "Heavy electrical load detected! Consider load-shifting heavy appliances (laundry/water heating) away from peak tariff hours."
        
    # Sub-metering decomposition in Watt-Hours (approx relative shares)
    sub1 = float(raw_inputs.get("Sub_metering_1", 0.0))
    sub2 = float(raw_inputs.get("Sub_metering_2", 0.0))
    sub3 = float(raw_inputs.get("Sub_metering_3", 0.0))
    
    # Active base power estimation
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
        
    # Generate 24-hour simulation curve based on current load
    hour_val = int(raw_inputs.get("Hour", 12))
    simulated_24h = []
    for h in range(24):
        # Time multiplier factor simulating daily load curves
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
