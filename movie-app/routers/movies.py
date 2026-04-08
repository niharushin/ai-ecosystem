from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Movie

router = APIRouter(prefix="/movies", tags=["Movies & Anime"])

class MovieCreate(BaseModel):
    title: str
    type: Optional[str] = "movie"
    genre: Optional[str] = ""
    total_episodes: Optional[int] = 0
    status: Optional[str] = "watching"

class MovieUpdate(BaseModel):
    status: Optional[str] = None
    rating: Optional[float] = None
    review: Optional[str] = None
    watched_episodes: Optional[int] = None

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(Movie).order_by(Movie.created_at.desc()).all()

@router.get("/anime")
def get_anime(db: Session = Depends(get_db)):
    return db.query(Movie).filter(Movie.type == "anime").all()

@router.get("/movies-only")
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).filter(Movie.type == "movie").all()

@router.post("/")
def add_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    new_movie = Movie(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@router.put("/{movie_id}")
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    existing = db.query(Movie).filter(Movie.id == movie_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie.dict(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"message": "Deleted successfully"}