from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Note

router = APIRouter(prefix="/notes", tags=["Notes"])

class NoteCreate(BaseModel):
    title: str
    content: str
    tag: Optional[str] = "general"

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tag: Optional[str] = None

@router.get("/")
def get_all_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()

@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.get("/search/{keyword}")
def search_notes(keyword: str, db: Session = Depends(get_db)):
    return db.query(Note).filter(
        Note.title.contains(keyword) | Note.content.contains(keyword)
    ).all()

@router.post("/")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(**note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.put("/{note_id}")
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    existing = db.query(Note).filter(Note.id == note_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in note.dict(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}