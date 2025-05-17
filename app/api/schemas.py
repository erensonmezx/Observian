# app/api/schemas.py

from pydantic import BaseModel
from datetime import datetime


class LogEventOut(BaseModel):
    id: int
    timestamp: datetime
    service_name: str
    status_code: int
    latency_ms: float
    
    class Config:
        orm_mode=True
        
    
