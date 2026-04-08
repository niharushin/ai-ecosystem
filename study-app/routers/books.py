from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Book

router = APIRouter(prefix="/books", tags=["Books"])

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = ""
    total_pages: Optional[int] = 0

class BookUpdate(BaseModel):
    pages_read: Optional[int] = None
    highlights: Optional[str] = None
    status: Optional[str] = None

@router.get("/")
def get_all_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/")
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{book_id}")
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    existing = db.query(Book).filter(Book.id == book_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    # Calculate progress percentage
    progress = 0
    if existing.total_pages > 0:
        progress = round((existing.pages_read / existing.total_pages) * 100, 1)
    return {"book": existing, "progress_percentage": progress}

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}