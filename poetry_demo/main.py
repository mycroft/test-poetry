"""main application file"""
import time

from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from utils.random_gen import get_random_number

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total number of requests to this API'
)

ENDPOINT_COUNTER = Counter(
    'app_endpoint_requests_total',
    'Total requests per endpoint',
    ['endpoint']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

@app.route('/')
@REQUEST_LATENCY.labels(endpoint='/').time()
def hello():
    """Hello World API endpoint"""
    REQUEST_COUNT.inc()
    ENDPOINT_COUNTER.labels(endpoint='/').inc()
    return 'Hello World!'

@app.route('/api/data')
@REQUEST_LATENCY.labels(endpoint='/app/data').time()
def get_data():
    """Data API endpoint"""
    REQUEST_COUNT.inc()
    ENDPOINT_COUNTER.labels(endpoint='/app/data').inc()

    duration = 0.01 * get_random_number()
    time.sleep(duration)  # Simulate work
    return {'status': 'success', 'data': 'example data', 'duration': duration}

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
