import time
import logging
import json
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


# POSITIVE CASE
log_json(
    int(time.time() * 1000),
    'User login succeeded: {"user":"alice","status":"success","timestamp":"'
    + datetime.now().isoformat()
    + '"}',
    logStreamName,
    "INFO",
)

# NEGATIVE CASE
log_json(
    int(time.time() * 1000),
    'User login failed: {"user":"bob","error":"invalid credentials","timestamp":"'
    + datetime.now().isoformat()
    + '"}',
    logStreamName,
    "ERROR",
)

# Additional test cases
log_json(
    int(time.time() * 1000),
    'API request processed: {"endpoint":"/api/users","method":"GET","status":200,"response_time":150}',
    logStreamName,
    "INFO",
)

log_json(
    int(time.time() * 1000),
    'Database connection error: {"error":"connection timeout","retry_count":3,"database":"users_db"}',
    logStreamName,
    "ERROR",
)
