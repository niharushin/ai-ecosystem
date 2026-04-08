from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from database import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    tag = Column(String(100), default="general")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(200))
    total_pages = Column(Integer, default=0)
    pages_read = Column(Integer, default=0)
    highlights = Column(Text, default="")
    status = Column(String(50), default="reading")  # reading, completed, paused
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Paper(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    authors = Column(String(300))
    link = Column(String(500))
    summary = Column(Text, default="")
    annotations = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(200), nullable=False)
    duration_minutes = Column(Float, default=0)
    notes = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AIChat(Base):
    __tablename__ = "ai_chats"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    user_answer = Column(Text, default="")
    ai_feedback = Column(Text, default="")
    topic = Column(String(200), default="general")
    score = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())