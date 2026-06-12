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

st.title("⚡ Smart Grid Energy Management")
st.write(
    "Predict household power consumption using PCA and Linear Regression."
)

col1, col2, col3 = st.columns(3)

with col1:
    Global_reactive_power = st.number_input("Global Reactive Power", value=0.418)
    Voltage = st.number_input("Voltage", value=234.84)
    Global_intensity = st.number_input("Global Intensity", value=18.4)
    Sub_metering_1 = st.number_input("Sub Metering 1", value=0.0)
    Sub_metering_2 = st.number_input("Sub Metering 2", value=1.0)

with col2:
    Sub_metering_3 = st.number_input("Sub Metering 3", value=17.0)
    Hour = st.number_input("Hour", value=18)
    Day = st.number_input("Day", value=16)
    Month = st.number_input("Month", value=12)
    Year = st.number_input("Year", value=2010)

with col3:
    Weekday = st.number_input("Weekday", value=4)
    Weekend = st.number_input("Weekend", value=0)
    Peak_Hour = st.number_input("Peak Hour", value=1)
    Previous_Power = st.number_input("Previous Power", value=4.216)
    Rolling_Mean_24 = st.number_input("Rolling Mean 24", value=1.091)

if st.button("Predict Consumption"):

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

    st.success(
        f"Predicted Power Consumption: {prediction[0]:.4f} kW"
    )
