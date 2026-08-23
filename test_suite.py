import energy_engine
from app import app as flask_app
import py_compile

def run_tests():
    print("--- 1. Testing Energy Engine Presets ---")
    for k, v in energy_engine.PRESETS.items():
        res = energy_engine.predict_consumption(v['data'])
        assert 'predicted_kw' in res, f"Failed on {k}"
        assert res['predicted_kw'] >= 0, f"Negative kW on {k}"
        print(f"Preset {k:20s} -> {res['predicted_kw']:.4f} kW | Tier: {res['tier']}")

    print("\n--- 2. Testing Flask Test Client ---")
    client = flask_app.test_client()
    r1 = client.get('/')
    assert r1.status_code == 200, f"GET / failed with {r1.status_code}"
    print("GET / -> 200 OK")

    r2 = client.post('/api/predict', json=energy_engine.PRESETS['morning_rush']['data'])
    assert r2.status_code == 200, f"POST /api/predict failed with {r2.status_code}"
    data = r2.get_json()
    assert data['success'] is True
    print(f"POST /api/predict -> 200 OK | Predicted: {data['data']['predicted_kw']} kW")

    print("\n--- 3. Testing Streamlit Compilation ---")
    py_compile.compile('streamlit_app.py', doraise=True)
    print("streamlit_app.py compiled cleanly with zero errors!")

    print("\n All Automated Verification Checks Passed Successfully!")

if __name__ == "__main__":
    run_tests()
