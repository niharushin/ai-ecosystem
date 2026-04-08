from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from database import Base

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    exercise = Column(String(200), nullable=False)
    sets = Column(Integer, default=0)
    reps = Column(Integer, default=0)
    duration_minutes = Column(Float, default=0)
    calories_burned = Column(Float, default=0)
    notes = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DailyGoal(Base):
    __tablename__ = "daily_goals"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(20), nullable=False)
    water_goal_liters = Column(Float, default=2.0)
    water_current_liters = Column(Float, default=0.0)
    sleep_goal_hours = Column(Float, default=8.0)
    sleep_actual_hours = Column(Float, default=0.0)
    workout_goal_minutes = Column(Float, default=30.0)
    workout_actual_minutes = Column(Float, default=0.0)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FitnessChat(Base):
    __tablename__ = "fitness_chats"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    ai_response = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())