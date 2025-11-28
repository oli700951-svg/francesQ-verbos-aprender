from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Verb
from app.schemas import VerbCreate, VerbOut

router = APIRouter(prefix="/verbs", tags=["verbs"])

@router.post("/", response_model=VerbOut)
def create_verb(verb: VerbCreate, db: Session = Depends(get_db)):
    db_verb = Verb(**verb.dict())
    db.add(db_verb)
    db.commit()
    db.refresh(db_verb)
    return db_verb

@router.get("/", response_model=list[VerbOut])
def list_verbs(db: Session = Depends(get_db)):
    return db.query(Verb).all()
