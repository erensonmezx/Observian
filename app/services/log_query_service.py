# app/services/log_query_service.py

from sqlalchemy.orm import Session
from sqlalchemy import and_, func, case
from app.models.models import LogEvent, Service
from typing import Optional, List
from datetime import datetime

def get_filtered_logs(
    db:Session,
    service_name: Optional[str]= None,
    status_code: Optional[int]= None,
    start_time: Optional[datetime]= None,
    end_time: Optional[datetime]= None,
    event_type: Optional[str] = None,
    limit: int= 20,
    offset: int= 0
):
    query = (
    db.query(LogEvent.id, LogEvent.timestamp, LogEvent.status_code, LogEvent.event_type,
             LogEvent.latency_ms, Service.name.label('service_name'))
    .join(Service, LogEvent.service_id == Service.id)
)
    
    filters = []
    
    if service_name:
        filters.append(Service.name == service_name)
    if status_code:
        filters.append(LogEvent.status_code == status_code)
    if start_time:
        filters.append(LogEvent.timestamp >= start_time)
    if end_time:
        filters.append(LogEvent.timestamp <= end_time)
    if event_type:
        filters.append(LogEvent.event_type == event_type)
    
    if filters:
        query = query.filter(and_(*filters))
        
    return (
        query
        .order_by(LogEvent.timestamp.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

def get_log_summary(db:Session):
    total_logs = db.query(func.count(LogEvent.id)).scalar()
    
    error_logs = db.query(func.count()).filter(LogEvent.status_code >= 500).scalar()
    
    avg_latency = db.query(func.avg(LogEvent.latency_ms)).scalar()
    
    status_counts = (
        db.query(LogEvent.status_code, func.count(LogEvent.id))
        .group_by(LogEvent.status_code)
        .all()
    )
    
    return {
        'total_logs':total_logs,
        'error_rate_percent':round((error_logs/total_logs), 2) if total_logs else 0,
        'status_code_breakdown':{code: count for code, count in status_counts},
    }