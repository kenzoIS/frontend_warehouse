# app.py (Flask backend)
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Handle file saving and processing here (e.g., saving to a folder or DB)
    return jsonify({"message": "File uploaded successfully!"})

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    name = data.get('name')
    flight_id = data.get('flightId')
    passenger_id = data.get('passengerId')

    # Logic for eligibility based on flight delay >= 2 hours or canceled
    is_eligible = False
    if flight_id == 'delayed' or flight_id == 'canceled':  # Example check
        is_eligible = True

    return jsonify({"isEligible": is_eligible})

if __name__ == '__main__':
    app.run(debug=True)
