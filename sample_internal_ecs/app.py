from flask import Flask, jsonify
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "internal_ecs"})

@app.route('/api/endpoint')
def api_endpoint():
    """Main API endpoint that receives GET requests"""
    timestamp = datetime.now().isoformat()
    
    # Log the incoming request
    logger.info(f"Received GET request at {timestamp}")
    
    # Create response payload
    response_payload = {
        "message": "Request was properly received by the internal ECS service",
        "timestamp": timestamp,
        "service": "sample_internal_ecs",
        "status": "success"
    }
    
    # Log the response being sent
    logger.info(f"Sending response: {response_payload}")
    
    return jsonify(response_payload)

@app.route('/')
def index():
    """Simple welcome page"""
    return jsonify({
        "message": "Internal ECS Service is running",
        "endpoints": {
            "health": "/health",
            "api": "/api/endpoint"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True) 