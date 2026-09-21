import logging
import os
import time
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
START_TIME = time.time()

@app.get("/")
def home():
    return jsonify({"message": "CI/CD demo application", "version": os.getenv("APP_VERSION", "dev")})

@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.get("/ready")
def ready():
    return jsonify({"status": "ready"}), 200

@app.get("/info")
def info():
    return jsonify({
        "environment": os.getenv("APP_ENV", "development"),
        "version": os.getenv("APP_VERSION", "dev"),
        "uptime_seconds": round(time.time() - START_TIME, 2),
    })

@app.post("/echo")
def echo():
    payload = request.get_json(silent=True) or {}
    logger.info("echo request received")
    return jsonify({"echo": payload}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
