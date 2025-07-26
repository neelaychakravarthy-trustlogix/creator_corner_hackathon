from flask import Flask, render_template, jsonify
import requests
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
INTERNAL_SERVICE_URL = os.getenv('INTERNAL_SERVICE_URL', 'http://localhost:5002')

@app.route('/')
def index():
    """Main page with button to send request to internal service"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "external_ecs"})

@app.route('/send-request')
def send_request():
    """Send GET request to internal service and log response"""
    try:
        logger.info(f"Sending request to internal service at: {INTERNAL_SERVICE_URL}")
        
        # Send GET request to internal service
        response = requests.get(f"{INTERNAL_SERVICE_URL}/api/endpoint", timeout=10)
        
        # Log the response
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response content: {response.text}")
        
        return jsonify({
            "success": True,
            "status_code": response.status_code,
            "response": response.text
        })
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending request to internal service: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 