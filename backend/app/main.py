from fastapi import FastAPI
from app.api import logs, metrics
from app.api.metrics import metrics_middleware
from app.api import control
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:8001",
    "https://erensonmezx.github.io"
],          # fine for testing; narrow later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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