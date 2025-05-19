# app/api/schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LogEventOut(BaseModel):
    id: int
    timestamp: datetime
    service_name: str
    status_code: int
    latency_ms: float
    event_type: Optional[str] = None
    
    class Config:
        orm_mode=True
        
    
