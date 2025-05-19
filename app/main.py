from fastapi import FastAPI
from app.api import logs, metrics
from app.api.metrics import metrics_middleware
from app.api import control

app = FastAPI()

app.middleware('http')(metrics_middleware)

app.include_router(logs.router)
app.include_router(metrics.router)
app.include_router(control.router)

@app.get("/")
def root():
    return {"message": "Welcome to Observian"}

@app.get("/health")
def health_check():
    return {"status": "ok"}