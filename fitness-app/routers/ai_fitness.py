from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests
from database import get_db
from models import FitnessChat, Workout, DailyGoal

router = APIRouter(prefix="/ai-fitness", tags=["AI Fitness Coach"])

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

class FitnessQuestion(BaseModel):
    question: str

def ask_ollama(prompt: str) -> str:
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=60)
        return response.json().get("response", "AI could not respond")
    except Exception as e:
        return f"Ollama not running. Start it with: ollama serve — Error: {str(e)}"

@router.post("/ask")
def ask_fitness_question(req: FitnessQuestion, db: Session = Depends(get_db)):
    prompt = f"""You are a personal fitness coach.
    Question: {req.question}
    Give practical, safe, and motivating fitness advice."""

    response = ask_ollama(prompt)
    chat = FitnessChat(question=req.question, ai_response=response)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return {"question": req.question, "ai_response": response}

@router.get("/weekly-report")
def weekly_fitness_report(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    workouts = db.query(Workout).filter(Workout.created_at >= week_ago).all()
    goals = db.query(DailyGoal).filter(DailyGoal.created_at >= week_ago).all()

    completed_goals = len([g for g in goals if g.completed])
    total_calories = sum(w.calories_burned for w in workouts)

    prompt = f"""You are a fitness coach giving a weekly report.
    This week stats:
    - Total workouts: {len(workouts)}
    - Total calories burned: {total_calories}
    - Goals completed: {completed_goals} out of {len(goals)} days
    - Exercises done: {list(set([w.exercise for w in workouts]))}

    Give an encouraging weekly summary and 3 specific tips to improve next week."""

    report = ask_ollama(prompt)
    return {
        "total_workouts": len(workouts),
        "total_calories": total_calories,
        "completed_goals": completed_goals,
        "ai_report": report
    }