from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

class Service(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    team_owner = Column(String, nullable=True)
    
    logs = relationship('LogEvent', back_populates='service')
    
    
class LogEvent(Base):
    __tablename__ = 'log_events'
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    status_code = Column(Integer, nullable=False)
    # e.g., PushEvent, PullRequestEvent
    event_type = Column(String, nullable=True)    
    # The latency of the service in milliseconds
    latency_ms = Column(Float, nullable=False)
    
    service = relationship('Service', back_populates='logs')
    

