from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.models import LogEvent, Service
from app.api.schemas import LogEventOut
from app.services.log_query_service import get_filtered_logs, get_log_summary
from typing import List, Optional
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# @router.get('/logs', response_model=List[LogEventOut])
# def get_logs(db: Session = Depends(get_db)):
#     results= (
#         db.query(LogEvent.id, LogEvent.timestamp, LogEvent.status_code, 
#                  LogEvent.latency_ms, Service.name.label('service_name'))
#         .join(Service, LogEvent.service_id == Service.id)
#         .order_by(LogEvent.timestamp.desc())
#         .limit(20)
#         .all()
#     )
#     return results

@router.get('/logs', response_model=List[LogEventOut])
def get_logs(
    service_name: Optional[str] = Query(None),
    status_code: Optional[int] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    limit: int = Query(20, gt=0),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return get_filtered_logs(
        db=db,
        service_name=service_name,
        status_code=status_code,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
        offset=offset
    )
    
@router.get('/logs/summary')
def log_summary(db:Session = Depends(get_db)):
    summary = get_log_summary(db)
    return JSONResponse(content=summary)

class LogEventIn(BaseModel):
    service_name: str
    status_code: int
    latency_ms: float
    
@router.post('/logs')
def create_log(log: LogEventIn, db:Session= Depends(get_db)):
    service = db.query(Service).filter(Service.name == log.service_name).first()
    
    if not service:
        return JSONResponse(status_code= 404, content= {'detail': 'Service not found'})

    new_log = LogEvent(
        service_id = service.id,
        status_code = log.status_code,
        latency_ms = log.latency_ms
    )    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {'id': new_log.id, 'status':'created'}
    

    