"""main application file"""

import time

from flask import Flask, Response, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

from utils.random_gen import get_random_number
from utils.producer import MessageProducer

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "app_requests_total", "Total number of requests to this API"
)

ENDPOINT_COUNTER = Counter(
    "app_endpoint_requests_total",
    "Total requests per endpoint",
    ["endpoint", "method"],
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint", "method"],
)


@app.route("/")
@REQUEST_LATENCY.labels(endpoint="/", method="GET").time()
def hello():
    """Hello World API endpoint"""
    REQUEST_COUNT.inc()
    ENDPOINT_COUNTER.labels(endpoint="/").inc()
    return "Hello World!"


@app.route("/api/data", methods=["GET"])
@REQUEST_LATENCY.labels(endpoint="/app/data", method="GET").time()
def get_data():
    """Data API endpoint"""
    REQUEST_COUNT.inc()
    ENDPOINT_COUNTER.labels(endpoint="/app/data").inc()

    duration = 0.01 * get_random_number()
    time.sleep(duration)  # Simulate work
    return {"status": "success", "data": "example data", "duration": duration}


@app.route("/api/data", methods=["POST"])
@REQUEST_LATENCY.labels(endpoint="/app/data", method="POST").time()
def post_data():
    """POST Data API endpoint"""
    REQUEST_COUNT.inc()
    ENDPOINT_COUNTER.labels(endpoint="/api/data", method="POST").inc()

    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    if "data" not in data or not isinstance(data["data"], str):
        return jsonify({"error": "Missing or invalid 'data' field"}), 400

    queue = MessageProducer()
    queue.send_message(data)

    duration = 0.01 * get_random_number()
    time.sleep(duration)  # Simulate work

    return {
        "status": "success",
        "received_data": data["data"],
        "duration": duration,
    }


@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
