from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import ActivityLog, Alert, WeeklyReport
from monitors.game_monitor import get_today_gaming_stats
from monitors.study_monitor import get_today_study_stats
from monitors.fitness_monitor import get_today_fitness_stats
from report import generate_weekly_report
from datetime import date

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Jarvis — Edge AI Core",
    description="Your personal AI that monitors and improves your life",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🤖 Jarvis is online!", "status": "monitoring"}

@app.get("/today")
def today_summary(db: Session = Depends(get_db)):
    today = str(date.today())
    logs = db.query(ActivityLog).filter(ActivityLog.date == today).all()
    gaming = sum(l.duration_minutes for l in logs if l.activity_type == "gaming")
    study = sum(l.duration_minutes for l in logs if l.activity_type == "study")
    movie = sum(l.duration_minutes for l in logs if l.activity_type == "movie")
    fitness = sum(l.duration_minutes for l in logs if l.activity_type == "fitness")
    return {
        "date": today,
        "gaming_minutes": gaming,
        "study_minutes": study,
        "movie_minutes": movie,
        "fitness_minutes": fitness,
        "gaming_stats": get_today_gaming_stats(),
        "study_stats": get_today_study_stats(),
        "fitness_stats": get_today_fitness_stats()
    }

@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.is_read == False).all()
    return {"unread_alerts": len(alerts), "alerts": alerts}

@app.post("/alerts/{alert_id}/read")
def mark_read(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.is_read = True
        db.commit()
    return {"message": "Alert marked as read"}

@app.get("/weekly-report")
def weekly_report():
    return generate_weekly_report()

@app.get("/gaming")
def gaming_stats():
    return get_today_gaming_stats()

@app.get("/study")
def study_stats():
    return get_today_study_stats()

@app.get("/fitness")
def fitness_stats():
    return get_today_fitness_stats()