from database import SessionLocal
from models import ActivityLog
from datetime import date

def get_today_study_stats():
    db = SessionLocal()
    try:
        today = str(date.today())
        logs = db.query(ActivityLog).filter(
            ActivityLog.date == today,
            ActivityLog.activity_type == "study"
        ).all()
        total_minutes = sum(l.duration_minutes for l in logs)
        return {
            "total_study_minutes": total_minutes,
            "total_study_hours": round(total_minutes / 60, 1),
            "sessions": len(logs),
            "status": "Great work! 🔥" if total_minutes >= 120 else "Need more study time! 📚"
        }
    finally:
        db.close()