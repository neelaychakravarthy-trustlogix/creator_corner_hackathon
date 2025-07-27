import time
import logging
import json
import random
from datetime import datetime

# JSON log format for better Datadog parsing
LOG_FILE = "custom.log"  # Local file in current directory

logStreamName = "service-logs/app-container/instance-001"
formatter = logging.Formatter("%(message)s")

handler = logging.FileHandler(LOG_FILE)
handler.setFormatter(formatter)

logger = logging.getLogger("my_json_logger")
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)


def log_json(ts, msg, stream, level="INFO"):
    """Enhanced logging function with JSON structure for Datadog"""
    # Create structured log entry
    log_entry = {
        "timestamp": ts,
        "message": msg,
        "logStreamName": stream,
        "level": level,
        "service": "log-generator",
        "source": "python",
        "host": "localhost",
    }

    # Convert to JSON format for file logging
    line = json.dumps(log_entry)
    logger.info(line)

    # Also log to console for debugging
    print(f"[{datetime.fromtimestamp(ts/1000).isoformat()}] {level}: {msg}")


def generate_random_log():
    """Generate a random log entry"""
    log_types = [
        # User authentication logs
        {
            "message": f'User login succeeded: {{"user":"{random.choice(["alice", "bob", "charlie", "diana", "eve"])}","status":"success","timestamp":"{datetime.now().isoformat()}"}}',
            "level": "INFO",
        },
        {
            "message": f'User login failed: {{"user":"{random.choice(["frank", "grace", "henry", "iris", "jack"])}","error":"{random.choice(["invalid credentials", "account locked", "expired password"])}","timestamp":"{datetime.now().isoformat()}"}}',
            "level": "ERROR",
        },
        # API request logs
        {
            "message": f'API request processed: {{"endpoint":"{random.choice(["/api/users", "/api/products", "/api/orders", "/api/auth"])}","method":"{random.choice(["GET", "POST", "PUT", "DELETE"])}","status":{random.choice([200, 201, 400, 401, 404, 500])},"response_time":{random.randint(50, 500)}}}',
            "level": "INFO",
        },
        # Database logs
        {
            "message": f'Database connection error: {{"error":"{random.choice(["connection timeout", "authentication failed", "database not found", "permission denied"])}","retry_count":{random.randint(1, 5)},"database":"{random.choice(["users_db", "products_db", "orders_db", "analytics_db"])}"}}',
            "level": "ERROR",
        },
        {
            "message": f'Database query executed: {{"query":"SELECT * FROM {random.choice(["users", "products", "orders", "logs"])}","execution_time":{random.randint(10, 200)},"rows_returned":{random.randint(0, 1000)}}}',
            "level": "INFO",
        },
        # System logs
        {
            "message": f'System resource usage: {{"cpu_percent":{random.randint(10, 95)},"memory_percent":{random.randint(20, 90)},"disk_usage":{random.randint(30, 85)},"timestamp":"{datetime.now().isoformat()}"}}',
            "level": "INFO",
        },
        {
            "message": f'System warning: {{"warning":"{random.choice(["high memory usage", "disk space low", "network latency high", "service restart"])}","severity":"{random.choice(["low", "medium", "high"])}","timestamp":"{datetime.now().isoformat()}"}}',
            "level": "WARN",
        },
        # Security logs
        {
            "message": f'Security alert: {{"alert":"{random.choice(["failed login attempt", "suspicious activity", "unauthorized access", "rate limit exceeded"])}","ip":"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}","timestamp":"{datetime.now().isoformat()}"}}',
            "level": "ERROR",
        },
    ]

    return random.choice(log_types)


def main():
    """Main function to continuously generate logs"""
    print("Starting log generator... Press Ctrl+C to stop")

    try:
        while True:
            # Generate random log
            log_data = generate_random_log()

            # Log the entry
            log_json(
                int(time.time() * 1000),
                log_data["message"],
                logStreamName,
                log_data["level"],
            )

            # Wait for 1 second
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nLog generator stopped.")


if __name__ == "__main__":
    main()
