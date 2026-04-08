from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import notes, books, papers, ai_tutor

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Study App API",
    description="Your personal AI-powered study assistant",
    version="1.0.0"
)

# Allow frontend to connect later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(notes.router)
app.include_router(books.router)
app.include_router(papers.router)
app.include_router(ai_tutor.router)

@app.get("/")
def root():
    return {
        "message": "Study App API is running! 🚀",
        "docs": "Go to /docs to see all endpoints"
    }