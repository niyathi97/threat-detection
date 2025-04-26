import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from sklearn.preprocessing import StandardScaler

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load model, scaler, and column config
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')
model_columns = joblib.load('model_columns.pkl')

# Threat dictionary with corresponding prevention steps
threat_info = {
    "normal": {
        "threat_name": "No Threat",
        "prevention": "No action needed."
    },
    "anomaly": {
        "threat_name": "Possible Anomaly",
        "prevention": "Analyze the network traffic and investigate potential attacks."
    }
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        df = pd.DataFrame(data if isinstance(data, list) else [data])

        # One-hot encode
        df = pd.get_dummies(df, columns=['protocol_type', 'service', 'flag'])
        df = df.reindex(columns=model_columns, fill_value=0)

        # Scale
        X_scaled = scaler.transform(df)

        # Predict + probability
        predictions = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)

        results = []
        for pred, prob in zip(predictions, probabilities):
            result = {
                'prediction': 'normal' if pred == 1 else 'anomaly',
                'confidence': {
                    'anomaly': f"{prob[0] * 100:.2f}%",
                    'normal': f"{prob[1] * 100:.2f}%"
                },
                'threat_info': threat_info['normal'] if pred == 1 else threat_info['anomaly']
            }
            results.append(result)

        return jsonify({'results': results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

