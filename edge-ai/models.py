from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    activity_type = Column(String(100), nullable=False)  # gaming, movie, study, fitness
    app_name = Column(String(200), default="")
    duration_minutes = Column(Float, default=0)
    date = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    alert_type = Column(String(100), default="warning")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WeeklyReport(Base):
    __tablename__ = "weekly_reports"
    id = Column(Integer, primary_key=True, index=True)
    week_start = Column(String(20), nullable=False)
    week_end = Column(String(20), nullable=False)
    total_study_minutes = Column(Float, default=0)
    total_gaming_minutes = Column(Float, default=0)
    total_movie_minutes = Column(Float, default=0)
    total_fitness_minutes = Column(Float, default=0)
    ai_report = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PCUsage(Base):
    __tablename__ = "pc_usage"
    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String(200), nullable=False)
    window_title = Column(String(500), default="")
    duration_minutes = Column(Float, default=0)
    date = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())