from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserProgress, ExamResult

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_progress = db.query(UserProgress).count()
    total_exams = db.query(ExamResult).count()
    return {
        "total_users": total_users,
        "total_progress_entries": total_progress,
        "total_exam_results": total_exams
    }
