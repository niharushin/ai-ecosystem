from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import get_db
from models import DailyGoal

router = APIRouter(prefix="/goals", tags=["Daily Goals"])

class GoalCreate(BaseModel):
    date: Optional[str] = str(date.today())
    water_goal_liters: Optional[float] = 2.0
    sleep_goal_hours: Optional[float] = 8.0
    workout_goal_minutes: Optional[float] = 30.0

class GoalUpdate(BaseModel):
    water_current_liters: Optional[float] = None
    sleep_actual_hours: Optional[float] = None
    workout_actual_minutes: Optional[float] = None

@router.get("/")
def get_all_goals(db: Session = Depends(get_db)):
    return db.query(DailyGoal).order_by(DailyGoal.created_at.desc()).all()

@router.get("/today")
def get_today_goal(db: Session = Depends(get_db)):
    today = str(date.today())
    goal = db.query(DailyGoal).filter(DailyGoal.date == today).first()
    if not goal:
        return {"message": "No goal set for today yet!"}
    return goal

@router.post("/")
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    new_goal = DailyGoal(**goal.dict())
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

@router.put("/{goal_id}")
def update_goal(goal_id: int, goal: GoalUpdate, db: Session = Depends(get_db)):
    existing = db.query(DailyGoal).filter(DailyGoal.id == goal_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Goal not found")
    for key, value in goal.dict(exclude_unset=True).items():
        setattr(existing, key, value)
    # Check if all goals completed
    if (existing.water_current_liters >= existing.water_goal_liters and
        existing.sleep_actual_hours >= existing.sleep_goal_hours and
        existing.workout_actual_minutes >= existing.workout_goal_minutes):
        existing.completed = True
    db.commit()
    db.refresh(existing)
    return existing