from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model safely
try:
    model = joblib.load("model.pkl")
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Model load error:", e)
    model = None

# Home route (test server)
@app.route('/')
def home():
    return "AI Server Running"

# Test route (to check deployment)
@app.route('/test')
def test():
    return "TEST OK"

# Main AI route
@app.route('/data', methods=['POST'])
def detect():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        voltage = float(data.get('voltage', 0))
        current = float(data.get('current', 0))
        power = float(data.get('power', 0))

        if model is None:
            return jsonify({"error": "Model not loaded"}), 500

        features = np.array([[voltage, current, power]])
        prediction = model.predict(features)

        status = "NORMAL"
        relay = "ON"

        if prediction[0] == -1:
            status = "THEFT"
            relay = "OFF"

        return jsonify({
            "status": status,
            "relay": relay
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run locally (Render uses gunicorn)
if __name__ == '__main__':
    app.run(debug=True)
