from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load files
model = joblib.load("model.pkl")
imputer = joblib.load("imputer.pkl")
scaler = joblib.load("scaler.pkl")
pca = joblib.load("pca.pkl")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    data = [
        float(request.form['Global_reactive_power']),
        float(request.form['Voltage']),
        float(request.form['Global_intensity']),
        float(request.form['Sub_metering_1']),
        float(request.form['Sub_metering_2']),
        float(request.form['Sub_metering_3']),
        float(request.form['Hour']),
        float(request.form['Day']),
        float(request.form['Month']),
        float(request.form['Year']),
        float(request.form['Weekday']),
        float(request.form['Weekend']),
        float(request.form['Peak_Hour']),
        float(request.form['Previous_Power']),
        float(request.form['Rolling_Mean_24'])
    ]

    features = np.array([data])

    features = imputer.transform(features)
    features = scaler.transform(features)
    features = pca.transform(features)

    prediction = model.predict(features)

    result = round(float(prediction[0]), 4)

    return render_template(
        'index.html',
        prediction_text=f'Predicted Power Consumption: {result} kW'
    )


if __name__ == '__main__':
    app.run(debug=True)