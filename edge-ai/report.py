import requests
from datetime import date, timedelta
from database import SessionLocal
from models import ActivityLog, WeeklyReport

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

def ask_ollama(prompt: str) -> str:
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        return response.json().get("response", "AI could not respond")
    except Exception as e:
        return f"Ollama not running — Error: {str(e)}"

def generate_weekly_report():
    db = SessionLocal()
    try:
        today = date.today()
        week_ago = today - timedelta(days=7)

        logs = db.query(ActivityLog).filter(
            ActivityLog.date >= str(week_ago)
        ).all()

        study_minutes = sum(l.duration_minutes for l in logs if l.activity_type == "study")
        gaming_minutes = sum(l.duration_minutes for l in logs if l.activity_type == "gaming")
        movie_minutes = sum(l.duration_minutes for l in logs if l.activity_type == "movie")
        fitness_minutes = sum(l.duration_minutes for l in logs if l.activity_type == "fitness")

        prompt = f"""You are Jarvis, a personal AI assistant giving a weekly life report.
        This week stats:
        - Study time: {round(study_minutes/60, 1)} hours
        - Gaming time: {round(gaming_minutes/60, 1)} hours
        - Movie/entertainment time: {round(movie_minutes/60, 1)} hours
        - Fitness time: {round(fitness_minutes/60, 1)} hours

        The user is a student applying for MEXT Kosen scholarship in 70 days.
        Give an honest, motivating weekly report with:
        1. What they did well
        2. What needs improvement
        3. Specific action plan for next week
        Be like a caring but strict mentor."""

        ai_report = ask_ollama(prompt)

        report = WeeklyReport(
            week_start=str(week_ago),
            week_end=str(today),
            total_study_minutes=study_minutes,
            total_gaming_minutes=gaming_minutes,
            total_movie_minutes=movie_minutes,
            total_fitness_minutes=fitness_minutes,
            ai_report=ai_report
        )
        db.add(report)
        db.commit()

        return {
            "week": f"{week_ago} to {today}",
            "study_hours": round(study_minutes/60, 1),
            "gaming_hours": round(gaming_minutes/60, 1),
            "movie_hours": round(movie_minutes/60, 1),
            "fitness_hours": round(fitness_minutes/60, 1),
            "ai_report": ai_report
        }
    finally:
        db.close()