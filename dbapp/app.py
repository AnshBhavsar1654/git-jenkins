from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "predictions.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define model
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    species = db.Column(db.String(50), nullable=False)

# Create tables at startup
with app.app_context():
    db.create_all()

@app.route('/save', methods=['POST'])
def save_prediction():
    data = request.get_json()
    new_pred = Prediction(
        sepal_length=data['sepal_length'],
        sepal_width=data['sepal_width'],
        petal_length=data['petal_length'],
        petal_width=data['petal_width'],
        species=data['species']
    )
    db.session.add(new_pred)
    db.session.commit()
    return jsonify({"status": "saved"}), 201

@app.route('/all', methods=['GET'])
def get_all():
    predictions = Prediction.query.all()
    results = [
        {
            "id": p.id,
            "sepal_length": p.sepal_length,
            "sepal_width": p.sepal_width,
            "petal_length": p.petal_length,
            "petal_width": p.petal_width,
            "species": p.species
        }
        for p in predictions
    ]
    return jsonify(results)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=6000)
