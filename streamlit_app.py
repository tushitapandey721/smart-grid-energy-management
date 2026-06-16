import streamlit as st
import numpy as np
import joblib

model = joblib.load("model.pkl")
imputer = joblib.load("imputer.pkl")
scaler = joblib.load("scaler.pkl")
pca = joblib.load("pca.pkl")

st.set_page_config(
    page_title="Smart Grid Energy Management",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
# ⚡ Smart Grid Energy Management System
### Household Electricity Consumption Prediction

This application predicts **household power consumption in kilowatts (kW)** using machine learning.

You do not need technical knowledge to use it.  
Just keep the default sample values or change them according to your electricity readings.
""")

st.divider()

with st.expander("📘 What does this project do?", expanded=True):
    st.write("""
    This system helps estimate how much electricity a household may consume based on:
    - Voltage and current intensity
    - Energy used by kitchen, laundry, and appliances
    - Time of day, day, month, and weekend status
    - Previous power usage pattern

    The model uses **PCA** to reduce feature complexity and **Linear Regression** to predict power consumption.
    """)

with st.expander("🧾 How to fill the form?"):
    st.write("""
    You can use the default values for testing.

    **Simple meaning of fields:**
    - **Voltage:** Electricity supply voltage, usually around 220–250.
    - **Global Intensity:** Current usage level.
    - **Sub Metering 1:** Kitchen-related electricity usage.
    - **Sub Metering 2:** Laundry-related usage.
    - **Sub Metering 3:** Water heater or AC-related usage.
    - **Hour:** Current hour from 0 to 23.
    - **Weekend:** Enter 1 for Saturday/Sunday, otherwise 0.
    - **Peak Hour:** Enter 1 if time is between 6 PM and 10 PM.
    """)

st.divider()

st.subheader("🔢 Enter Electricity Usage Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⚙️ Electrical Readings")
    Global_reactive_power = st.number_input(
        "Global Reactive Power",
        value=0.418,
        help="Reactive power consumed by the household."
    )
    Voltage = st.number_input(
        "Voltage",
        value=234.84,
        help="Voltage level of electricity supply."
    )
    Global_intensity = st.number_input(
        "Global Intensity",
        value=18.4,
        help="Current intensity in amperes."
    )
    Sub_metering_1 = st.number_input(
        "Sub Metering 1 - Kitchen",
        value=0.0,
        help="Electricity used by kitchen appliances."
    )
    Sub_metering_2 = st.number_input(
        "Sub Metering 2 - Laundry",
        value=1.0,
        help="Electricity used by laundry appliances."
    )

with col2:
    st.markdown("### 🏠 Appliance Usage")
    Sub_metering_3 = st.number_input(
        "Sub Metering 3 - Heater/AC",
        value=17.0,
        help="Electricity used by water heater or air conditioner."
    )
    Previous_Power = st.number_input(
        "Previous Power Usage",
        value=4.216,
        help="Power consumption recorded in the previous minute."
    )
    Rolling_Mean_24 = st.number_input(
        "24-Hour Average Power Usage",
        value=1.091,
        help="Average power usage over the last 24 hours."
    )

with col3:
    st.markdown("### 🕒 Time Information")
    Hour = st.number_input(
        "Hour of Day",
        min_value=0,
        max_value=23,
        value=18,
        help="Enter hour from 0 to 23."
    )
    Day = st.number_input(
        "Day of Month",
        min_value=1,
        max_value=31,
        value=16
    )
    Month = st.number_input(
        "Month",
        min_value=1,
        max_value=12,
        value=12
    )
    Year = st.number_input(
        "Year",
        value=2010
    )
    Weekday = st.number_input(
        "Weekday",
        min_value=0,
        max_value=6,
        value=4,
        help="Monday = 0, Sunday = 6."
    )
    Weekend = st.selectbox(
        "Is it Weekend?",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )
    Peak_Hour = st.selectbox(
        "Is it Peak Hour?",
        options=[0, 1],
        format_func=lambda x: "Yes, evening peak time" if x == 1 else "No"
    )

st.divider()

if st.button("🔮 Predict Power Consumption", use_container_width=True):

    features = np.array([[
        Global_reactive_power,
        Voltage,
        Global_intensity,
        Sub_metering_1,
        Sub_metering_2,
        Sub_metering_3,
        Hour,
        Day,
        Month,
        Year,
        Weekday,
        Weekend,
        Peak_Hour,
        Previous_Power,
        Rolling_Mean_24
    ]])

    features = imputer.transform(features)
    features = scaler.transform(features)
    features = pca.transform(features)

    prediction = model.predict(features)
    result = float(prediction.ravel()[0])

    st.success(f"⚡ Predicted Power Consumption: {result:.4f} kW")

    st.info("""
    This value represents the estimated household electricity demand based on the entered readings.
    Higher values indicate higher expected electricity usage.
    """)

    if result < 1:
        st.markdown("### 🟢 Usage Level: Low")
        st.write("Electricity consumption is low.")
    elif result < 3:
        st.markdown("### 🟡 Usage Level: Moderate")
        st.write("Electricity consumption is normal/moderate.")
    else:
        st.markdown("### 🔴 Usage Level: High")
        st.write("Electricity consumption is high. This may indicate peak appliance usage.")

st.divider()

st.markdown("""
### 📌 Project Summary

**Technology Used:** Python, Streamlit, PCA, Linear Regression, Scikit-learn  
**Dataset:** Individual Household Electric Power Consumption Dataset  
**Purpose:** To support smart grid energy management by predicting household electricity usage.
""")