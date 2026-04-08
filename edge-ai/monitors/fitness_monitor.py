from database import SessionLocal
from models import ActivityLog
from datetime import date

def get_today_fitness_stats():
    db = SessionLocal()
    try:
        today = str(date.today())
        logs = db.query(ActivityLog).filter(
            ActivityLog.date == today,
            ActivityLog.activity_type == "fitness"
        ).all()
        total_minutes = sum(l.duration_minutes for l in logs)
        return {
            "total_fitness_minutes": total_minutes,
            "sessions": len(logs),
            "status": "Great workout! 💪" if total_minutes >= 30 else "Don't skip the gym bro! 😤"
        }
    finally:
        db.close()