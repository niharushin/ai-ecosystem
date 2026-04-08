from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import movies, watch_sessions, ai_movies

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie & Anime Tracker API",
    description="Track your movies and anime with AI recommendations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(watch_sessions.router)
app.include_router(ai_movies.router)

@app.get("/")
def root():
    return {
        "message": "Movie & Anime Tracker API is running! 🎬",
        "docs": "Go to /docs to see all endpoints"
    }