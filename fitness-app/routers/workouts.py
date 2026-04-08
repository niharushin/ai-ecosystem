from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Workout

router = APIRouter(prefix="/workouts", tags=["Workouts"])

class WorkoutCreate(BaseModel):
    exercise: str
    sets: Optional[int] = 0
    reps: Optional[int] = 0
    duration_minutes: Optional[float] = 0
    calories_burned: Optional[float] = 0
    notes: Optional[str] = ""

@router.get("/")
def get_all_workouts(db: Session = Depends(get_db)):
    return db.query(Workout).order_by(Workout.created_at.desc()).all()

@router.post("/")
def log_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    new_workout = Workout(**workout.dict())
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout

@router.get("/summary")
def workout_summary(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    workouts = db.query(Workout).filter(Workout.created_at >= week_ago).all()
    total_calories = sum(w.calories_burned for w in workouts)
    total_minutes = sum(w.duration_minutes for w in workouts)
    return {
        "total_workouts_this_week": len(workouts),
        "total_calories_burned": total_calories,
        "total_minutes_exercised": total_minutes,
        "workouts": workouts
    }

@router.delete("/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()
    return {"message": "Workout deleted successfully"}