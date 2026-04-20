from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

@app.route('/')
def home():
    return "AI Server Running"

@app.route('/data', methods=['POST'])
def detect():
    data = request.json

    voltage = float(data['voltage'])
    current = float(data['current'])
    power = float(data['power'])

    features = np.array([[voltage, current, power]])
    prediction = model.predict(features)

    status = "NORMAL"
    relay = "ON"

    if prediction[0] == -1:
        status = "THEFT"
        relay = "OFF"

    return jsonify({"status": status, "relay": relay})
