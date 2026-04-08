from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import workouts, goals, ai_fitness

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness App API",
    description="Your personal AI-powered fitness coach",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workouts.router)
app.include_router(goals.router)
app.include_router(ai_fitness.router)

@app.get("/")
def root():
    return {
        "message": "Fitness App API is running! 💪",
        "docs": "Go to /docs to see all endpoints"
    }