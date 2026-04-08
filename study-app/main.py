from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os
from database import engine, Base
from routers import notes, books, papers, ai_tutor

load_dotenv()

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Study App API",
    description="Your personal AI-powered study assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router, dependencies=[Depends(verify_api_key)])
app.include_router(books.router, dependencies=[Depends(verify_api_key)])
app.include_router(papers.router, dependencies=[Depends(verify_api_key)])
app.include_router(ai_tutor.router, dependencies=[Depends(verify_api_key)])

@app.get("/")
def root():
    return {
        "message": "Study App API is running! 🚀",
        "docs": "Go to /docs to see all endpoints"
    }