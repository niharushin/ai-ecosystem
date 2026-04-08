from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import requests
from database import get_db
from models import AIChat

router = APIRouter(prefix="/ai-tutor", tags=["AI Tutor"])

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

class QuestionRequest(BaseModel):
    topic: str
    question: str

class AnswerRequest(BaseModel):
    chat_id: int
    user_answer: str

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
def ask_question(req: QuestionRequest, db: Session = Depends(get_db)):
    prompt = f"""You are a helpful study tutor. 
    Topic: {req.topic}
    Question from student: {req.question}
    Give a clear, educational answer."""
    
    ai_response = ask_ollama(prompt)
    
    chat = AIChat(
        question=req.question,
        ai_feedback=ai_response,
        topic=req.topic
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return {"chat_id": chat.id, "question": req.question, "ai_response": ai_response}

@router.post("/submit-answer")
def submit_answer(req: AnswerRequest, db: Session = Depends(get_db)):
    chat = db.query(AIChat).filter(AIChat.id == req.chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    prompt = f"""You are a study tutor analysing a student's answer.
    Original question: {chat.question}
    Student's answer: {req.user_answer}
    
    Please:
    1. Give a score out of 10
    2. Point out what they got right
    3. Point out what they got wrong or missed
    4. Give suggestions to improve
    
    Be encouraging and educational."""
    
    feedback = ask_ollama(prompt)
    
    chat.user_answer = req.user_answer
    chat.ai_feedback = feedback
    db.commit()
    db.refresh(chat)
    return {"feedback": feedback, "chat": chat}

@router.get("/history")
def get_chat_history(db: Session = Depends(get_db)):
    return db.query(AIChat).order_by(AIChat.created_at.desc()).all()

@router.get("/weekly-report")
def weekly_report(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    chats = db.query(AIChat).filter(AIChat.created_at >= week_ago).all()
    
    if not chats:
        return {"message": "No study sessions this week!"}
    
    topics = list(set([c.topic for c in chats]))
    summary = f"""Student studied these topics this week: {', '.join(topics)}.
    Total questions asked: {len(chats)}.
    Give a weekly study analysis and 3 specific improvement tips."""
    
    report = ask_ollama(summary)
    return {"sessions": len(chats), "topics": topics, "report": report}