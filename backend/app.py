from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health')
def health():
    return jsonify({
        "status": "ok",
        "message": "Backend is running, API is healthy."
    })

@app.route('/api/data')
def data():
    return jsonify({
        "project": "CSC468 Project",
        "stack": ["Nginx", "Flask", "Docker"],
        "message": "Sample response from the backend API. Hello!"
    })

app.run(host='0.0.0.0', port=5000)