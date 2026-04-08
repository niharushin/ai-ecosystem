from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from database import Base

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    type = Column(String(50), default="movie")  # movie or anime
    genre = Column(String(200), default="")
    status = Column(String(50), default="watching")  # watching, completed, planned
    rating = Column(Float, default=0)
    review = Column(Text, default="")
    total_episodes = Column(Integer, default=0)
    watched_episodes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WatchSession(Base):
    __tablename__ = "watch_sessions"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, nullable=False)
    title = Column(String(300), nullable=False)
    duration_minutes = Column(Float, default=0)
    date = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WatchLimit(Base):
    __tablename__ = "watch_limits"
    id = Column(Integer, primary_key=True, index=True)
    daily_limit_minutes = Column(Float, default=120)
    movies_per_day = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())