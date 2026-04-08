from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests
from database import get_db
from models import WatchSession, Movie

router = APIRouter(prefix="/ai-movies", tags=["AI Movie Assistant"])

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

class RecommendRequest(BaseModel):
    genre: str
    mood: str

def ask_ollama(prompt: str) -> str:
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=60)
        return response.json().get("response", "AI could not respond")
    except Exception as e:
        return f"Ollama not running — Error: {str(e)}"

@router.post("/recommend")
def recommend(req: RecommendRequest):
    prompt = f"""You are a movie and anime expert.
    User mood: {req.mood}
    Preferred genre: {req.genre}
    Recommend 5 movies or anime with a short reason for each.
    Be specific and enthusiastic!"""
    return {"recommendations": ask_ollama(prompt)}

@router.get("/weekly-report")
def weekly_report(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    sessions = db.query(WatchSession).filter(WatchSession.created_at >= week_ago).all()
    total_minutes = sum(s.duration_minutes for s in sessions)
    titles = [s.title for s in sessions]

    prompt = f"""You are a lifestyle coach reviewing someone's watching habits.
    This week they watched: {titles}
    Total time: {round(total_minutes/60, 1)} hours
    Give a fun but honest review of their watching habits and suggest a healthy balance with study and fitness."""

    return {
        "total_hours": round(total_minutes/60, 1),
        "watched": titles,
        "ai_report": ask_ollama(prompt)
    }

@router.get("/limit-check")
def check_limit(db: Session = Depends(get_db)):
    from datetime import date
    today = str(date.today())
    sessions = db.query(WatchSession).filter(WatchSession.date == today).all()
    total_minutes = sum(s.duration_minutes for s in sessions)
    total_movies = len(sessions)

    if total_movies >= 2:
        message = f"🚨 Bro you watched {total_movies} movies today! Go study or sleep 😭"
    elif total_minutes >= 120:
        message = f"⚠️ {round(total_minutes/60,1)} hours of watching today! Take a break bro!"
    else:
        message = f"✅ You're good! {total_movies} movies, {total_minutes} mins today."

    return {"message": message, "total_movies": total_movies, "total_minutes": total_minutes}