from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import os
import requests
from waitress import serve

app = Flask(__name__)

# Load ML model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

LABEL_TO_SPECIES = {
    0: 'setosa',
    1: 'versicolor',
    2: 'virginica'
}

DB_SERVICE_URL = "http://cntdbapp:6000"  # DB microservice endpoint

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload received'}), 400

    try:
        sl = float(data.get('sepal_length'))
        sw = float(data.get('sepal_width'))
        pl = float(data.get('petal_length'))
        pw = float(data.get('petal_width'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input values'}), 400

    X = np.array([[sl, sw, pl, pw]])
    pred_label = int(model.predict(X)[0])
    species = LABEL_TO_SPECIES.get(pred_label, 'unknown')

    # Save prediction in DB service
    requests.post(f"{DB_SERVICE_URL}/save", json={
        "sepal_length": sl,
        "sepal_width": sw,
        "petal_length": pl,
        "petal_width": pw,
        "species": species
    })

    return jsonify({'prediction_species': species})

@app.route('/all', methods=['GET'])
def dis_recs():
    response = requests.get(f"{DB_SERVICE_URL}/all")
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch data from DB service'}), 500

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)