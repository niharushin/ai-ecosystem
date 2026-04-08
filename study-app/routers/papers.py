from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Paper

router = APIRouter(prefix="/papers", tags=["Papers"])

class PaperCreate(BaseModel):
    title: str
    authors: Optional[str] = ""
    link: Optional[str] = ""
    summary: Optional[str] = ""

class PaperUpdate(BaseModel):
    summary: Optional[str] = None
    annotations: Optional[str] = None

@router.get("/")
def get_all_papers(db: Session = Depends(get_db)):
    return db.query(Paper).all()

@router.get("/{paper_id}")
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@router.post("/")
def add_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    new_paper = Paper(**paper.dict())
    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)
    return new_paper

@router.put("/{paper_id}")
def update_paper(paper_id: int, paper: PaperUpdate, db: Session = Depends(get_db)):
    existing = db.query(Paper).filter(Paper.id == paper_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Paper not found")
    for key, value in paper.dict(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/{paper_id}")
def delete_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    db.delete(paper)
    db.commit()
    return {"message": "Paper deleted successfully"}