from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
import random
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.auth import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/practice", tags=["practice"])
sujetos = ["je", "tu", "il/elle", "nous", "vous", "ils/elles"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/individual")
def practice_individual(
    request: schemas.IndividualPracticeRequest,
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    verb = db.query(models.Verb).filter(models.Verb.id == request.verb_id).first()
    if not verb:
        raise HTTPException(status_code=404, detail="Verbo no encontrado")

    presente_answers = [
        request.presente.je, request.presente.tu, request.presente.il,
        request.presente.nous, request.presente.vous, request.presente.ils
    ]
    presente_correct = [
        verb.presente_je, verb.presente_tu, verb.presente_il,
        verb.presente_nous, verb.presente_vous, verb.presente_ils
    ]
    presente_score = sum(1 for u, c in zip(presente_answers, presente_correct) if u.strip().lower() == c.lower())
    passe_score = 1 if request.passe.je.strip().lower() == verb.passe_compose.lower() else 0

    total_correct = presente_score + passe_score
    total_questions = 7

    progress = db.query(models.UserProgress).filter_by(user_id=current_user_id, verb_id=request.verb_id).first()
    if not progress:
        progress = models.UserProgress(user_id=current_user_id, verb_id=request.verb_id)
        db.add(progress)
    progress.total_attempts += total_questions
    progress.correct_attempts += total_correct
    db.commit()

    return {
        "score": total_correct,
        "total": total_questions,
        "porcentaje": round(total_correct / total_questions * 100, 1)
    }

@router.get("/exam")
def get_exam(db: Session = Depends(database.get_db)):
    verbs = db.query(models.Verb).all()
    if not verbs:
        raise HTTPException(status_code=404, detail="No hay verbos disponibles")
    questions = []
    for _ in range(min(10, len(verbs))):
        verb = random.choice(verbs)
        if random.choice([True, False]):
            i = random.randint(0, 5)
            questions.append({
                "question": f"Conjuga '{verb.infinitive}' en presente con '{sujetos[i]}':",
                "answer": [verb.presente_je, verb.presente_tu, verb.presente_il,
                          verb.presente_nous, verb.presente_vous, verb.presente_ils][i],
                "verb_id": verb.id,
                "type": "presente"
            })
        else:
            questions.append({
                "question": f"¿Cómo se dice 'je' + '{verb.spanish}' en passé composé?",
                "answer": verb.passe_compose,
                "verb_id": verb.id,
                "type": "passe"
            })
    return {"questions": questions}
