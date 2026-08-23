import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import energy_engine

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    # Initial default preset and dynamic time
    default_preset = energy_engine.PRESETS["standard_balanced"]["data"]
    time_info = energy_engine.derive_time_features()
    
    # Merge current time features into default data
    initial_data = dict(default_preset)
    initial_data.update(time_info)
    
    return render_template(
        "index.html",
        presets=energy_engine.PRESETS,
        form_data=initial_data,
        result=None
    )

@app.route("/predict", methods=["POST"])
def predict():
    form_data = request.form.to_dict()
    
    # Auto derive time if user used datetime-local input
    custom_dt = form_data.get("custom_datetime")
    if custom_dt:
        try:
            dt_parsed = datetime.fromisoformat(custom_dt)
            derived = energy_engine.derive_time_features(dt_parsed)
            form_data.update(derived)
        except Exception:
            pass
            
    result = energy_engine.predict_consumption(form_data)
    
    return render_template(
        "index.html",
        presets=energy_engine.PRESETS,
        form_data=form_data,
        result=result
    )

@app.route("/api/predict", methods=["POST"])
def api_predict():
    payload = request.get_json(force=True, silent=True) or request.form.to_dict()
    if not payload:
        return jsonify({"success": False, "error": "No input payload received"}), 400
        
    custom_dt = payload.get("custom_datetime")
    if custom_dt:
        try:
            dt_parsed = datetime.fromisoformat(custom_dt)
            derived = energy_engine.derive_time_features(dt_parsed)
            payload.update(derived)
        except Exception:
            pass
            
    try:
        analytics = energy_engine.predict_consumption(payload)
        return jsonify({
            "success": True,
            "data": analytics,
            "inputs_echo": payload
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/presets", methods=["GET"])
def api_presets():
    return jsonify(energy_engine.PRESETS)

@app.route("/api/time", methods=["GET"])
def api_time():
    return jsonify(energy_engine.derive_time_features())

if __name__ == "__main__":
    app.run(debug=True, port=5000)
