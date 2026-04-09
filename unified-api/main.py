from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

app = FastAPI(
    title="AI Ecosystem — Unified API",
    description="One API to rule them all 😈",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STUDY_APP = "https://study-app-qwlh.onrender.com"
FITNESS_APP = "https://fitness-app-2li2.onrender.com"
MOVIE_APP = "https://movie-app-fjwu.onrender.com"
JARVIS = "https://jarvis-edge-ai.onrender.com"
HEADERS = {"X-API-Key": API_KEY}

def fetch(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        return response.json()
    except:
        return {"error": f"Service at {url} is not running"}

@app.get("/")
def root():
    return {
        "message": "🤖 AI Ecosystem is ONLINE!",
        "apps": {
            "study_app": STUDY_APP,
            "fitness_app": FITNESS_APP,
            "movie_app": MOVIE_APP,
            "jarvis": JARVIS
        }
    }

@app.get("/dashboard", dependencies=[Depends(verify_api_key)])
def dashboard():
    jarvis_today = fetch(f"{JARVIS}/today")
    gaming_stats = fetch(f"{JARVIS}/gaming")
    study_stats = fetch(f"{JARVIS}/study")
    fitness_stats = fetch(f"{JARVIS}/fitness")
    alerts = fetch(f"{JARVIS}/alerts")
    notes = fetch(f"{STUDY_APP}/notes/")
    books = fetch(f"{STUDY_APP}/books/")
    workouts = fetch(f"{FITNESS_APP}/workouts/summary")
    movies = fetch(f"{MOVIE_APP}/watch-sessions/today")
    return {
        "today_summary": jarvis_today,
        "alerts": alerts,
        "study": {
            "stats": study_stats,
            "total_notes": len(notes) if isinstance(notes, list) else 0,
            "total_books": len(books) if isinstance(books, list) else 0,
        },
        "fitness": {
            "stats": fitness_stats,
            "weekly_workouts": workouts
        },
        "entertainment": {
            "gaming": gaming_stats,
            "movies_today": movies
        }
    }

@app.get("/weekly-report", dependencies=[Depends(verify_api_key)])
def full_weekly_report():
    jarvis_report = fetch(f"{JARVIS}/weekly-report")
    study_report = fetch(f"{STUDY_APP}/ai-tutor/weekly-report")
    fitness_report = fetch(f"{FITNESS_APP}/ai-fitness/weekly-report")
    movie_report = fetch(f"{MOVIE_APP}/ai-movies/weekly-report")
    return {
        "jarvis_analysis": jarvis_report,
        "study_report": study_report,
        "fitness_report": fitness_report,
        "entertainment_report": movie_report
    }

@app.get("/health")
def health_check():
    return {
        "study_app": "online" if "error" not in fetch(f"{STUDY_APP}/") else "offline",
        "fitness_app": "online" if "error" not in fetch(f"{FITNESS_APP}/") else "offline",
        "movie_app": "online" if "error" not in fetch(f"{MOVIE_APP}/") else "offline",
        "jarvis": "online" if "error" not in fetch(f"{JARVIS}/") else "offline",
    }