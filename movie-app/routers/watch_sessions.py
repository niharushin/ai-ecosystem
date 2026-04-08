from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import get_db
from models import WatchSession, WatchLimit

router = APIRouter(prefix="/watch-sessions", tags=["Watch Sessions"])

class SessionCreate(BaseModel):
    movie_id: int
    title: str
    duration_minutes: float
    date: Optional[str] = str(date.today())

@router.get("/")
def get_all_sessions(db: Session = Depends(get_db)):
    return db.query(WatchSession).order_by(WatchSession.created_at.desc()).all()

@router.get("/today")
def get_today_sessions(db: Session = Depends(get_db)):
    today = str(date.today())
    sessions = db.query(WatchSession).filter(WatchSession.date == today).all()
    total_minutes = sum(s.duration_minutes for s in sessions)
    total_movies = len(sessions)

    # Check limits
    limit = db.query(WatchLimit).first()
    warning = None
    if limit:
        if total_movies >= limit.movies_per_day:
            warning = f"⚠️ You've watched {total_movies} movie/anime today! Limit is {limit.movies_per_day}"
        if total_minutes >= limit.daily_limit_minutes:
            warning = f"⚠️ You've watched {total_minutes} mins today! Limit is {limit.daily_limit_minutes} mins"

    return {
        "sessions": sessions,
        "total_minutes_today": total_minutes,
        "total_movies_today": total_movies,
        "warning": warning
    }

@router.post("/")
def log_session(session: SessionCreate, db: Session = Depends(get_db)):
    new_session = WatchSession(**session.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/weekly-summary")
def weekly_summary(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    sessions = db.query(WatchSession).filter(WatchSession.created_at >= week_ago).all()
    total_minutes = sum(s.duration_minutes for s in sessions)
    return {
        "total_sessions": len(sessions),
        "total_hours_watched": round(total_minutes / 60, 1),
        "sessions": sessions
    }