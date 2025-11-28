from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

class Verb(Base):
    __tablename__ = "verbs"
    id = Column(Integer, primary_key=True, index=True)
    spanish = Column(String, index=True)
    infinitive = Column(String, index=True)
    presente_je = Column(String)
    presente_tu = Column(String)
    presente_il = Column(String)
    presente_nous = Column(String)
    presente_vous = Column(String)
    presente_ils = Column(String)
    passe_compose = Column(String)

class UserProgress(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    verb_id = Column(Integer, ForeignKey("verbs.id"))
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)

    user = relationship("User", backref="progress")
    verb = relationship("Verb")

class ExamResult(Base):
    __tablename__ = "exam_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer)
    total = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
