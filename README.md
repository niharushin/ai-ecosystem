# 🤖 AI Ecosystem — Personal Jarvis

A personal AI ecosystem that monitors and improves your life.
Built with FastAPI, SQLite, and Phi-3 Mini (offline AI).

## 🚀 Apps
- **Study App** — Notes, Books, Papers, AI Tutor
- **Fitness App** — Workouts, Goals, AI Coach
- **Movie/Anime App** — Tracker, Watch Limits, AI Recommendations
- **Edge AI Core (Jarvis)** — Monitors PC, Gaming, Study, Fitness

## 🧠 Features
- 100% offline AI using Phi-3 Mini
- Runs on low-end devices
- Weekly AI improvement reports
- Real-time PC activity monitoring
- Unified dashboard API

## 🛠️ Tech Stack
- Python, FastAPI, SQLAlchemy, SQLite
- Ollama + Phi-3 Mini (offline AI)
- Psutil (PC monitoring)

## 🏃 How to Run
```bash
# Study App
cd study-app && uvicorn main:app --reload --port 8000

# Fitness App
cd fitness-app && uvicorn main:app --reload --port 8001

# Movie App
cd movie-app && uvicorn main:app --reload --port 8002

# Jarvis
cd edge-ai && uvicorn main:app --reload --port 8003

# Unified API
cd unified-api && uvicorn main:app --reload --port 8004
```