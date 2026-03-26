from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Health check endpoint - useful for verifying the backend is reachable
@app.route('/api/health')
def health():
    return jsonify({
        "status": "ok",
        "message": "Backend is running"
    })

# Sample data endpoint - frontend will fetch and display this
@app.route('/api/data')
def data():
    return jsonify({
        "project": "CSC468-project",
        "stack": ["Nginx", "Flask", "Docker"],
        "message": "Hello from the backend!"
    })

# Always run - no __main__ check
app.run(host='0.0.0.0', port=5000)