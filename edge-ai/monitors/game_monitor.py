from database import SessionLocal
from models import ActivityLog
from datetime import date

def get_today_gaming_stats():
    db = SessionLocal()
    try:
        today = str(date.today())
        logs = db.query(ActivityLog).filter(
            ActivityLog.date == today,
            ActivityLog.activity_type == "gaming"
        ).all()
        total_minutes = sum(l.duration_minutes for l in logs)
        return {
            "total_gaming_minutes": total_minutes,
            "total_gaming_hours": round(total_minutes / 60, 1),
            "sessions": len(logs),
            "warning": "Too much gaming bro! 😭" if total_minutes >= 120 else "Gaming time is fine ✅"
        }
    finally:
        db.close()