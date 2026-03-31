import pickle
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model once at startup
MODEL_PATH = os.path.join(os.getcwd(), 'saved_model.pkl')

def load_model():
    try:
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        return None

model_data = load_model()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model_data is not None})

@app.route('/api/predict', methods=['POST'])
def predict():
    if model_data is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        
        # Extract features in order
        features = [
            float(data.get('study_hours', 0)),
            float(data.get('attendance', 0)),
            float(data.get('internal_marks', 0)),
            float(data.get('sleep_hours', 0)),
            float(data.get('assignment_completion', 0)),
            float(data.get('previous_marks', 0)),
            float(data.get('class_participation', 0)),
            float(data.get('internet_access', 1 if data.get('internet_access') else 0)),
            float(data.get('extra_classes', 0)),
        ]
        
        # Scale and predict
        model = model_data['model']
        scaler = model_data['scaler']
        
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)[0]
        
        # Determine grade
        if prediction >= 90:
            grade = "Excellent"
        elif prediction >= 75:
            grade = "Good"
        elif prediction >= 60:
            grade = "Average"
        else:
            grade = "Poor"
        
        response = {
            'prediction': float(prediction),
            'grade': grade,
            'success': True
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Student Performance Predictor API', 'version': '1.0'}), 200

if __name__ == '__main__':
    app.run(debug=False)
