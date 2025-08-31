# app/api/metrics.py

from fastapi import APIRouter, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

router = APIRouter()

REQUEST_COUNT = Counter(
    'observian_requests_total', 'Total number of requests', ['method','endpoint']
)
REQUEST_LATENCY = Histogram(
    'observian_request_latency_seconds', 'Latency in seconds', ['endpoint']
)
ERROR_COUNT = Counter(
    'observian_error_count', 'Total number of errors', ['endpoint', 'status_code']
)

async def metrics_middleware(request: Request, call_next):
    start_time= time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        ERROR_COUNT.labels(endpoint=request.url.path, status_code='500').inc()
        raise e
    
    latency = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)
    
    if response.status_code >= 500:
        ERROR_COUNT.labels(endpoint=request.url.path, status_code=str(response.status_code)).inc()
    
    return response

@router.get('/metrics')
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
