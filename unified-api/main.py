from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

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

# All app URLs
STUDY_APP = "http://127.0.0.1:8000"
FITNESS_APP = "http://127.0.0.1:8001"
MOVIE_APP = "http://127.0.0.1:8002"
JARVIS = "http://127.0.0.1:8003"

def fetch(url):
    try:
        response = requests.get(url, timeout=5)
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

@app.get("/dashboard")
def dashboard():
    # Fetch data from all apps at once
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

@app.get("/weekly-report")
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