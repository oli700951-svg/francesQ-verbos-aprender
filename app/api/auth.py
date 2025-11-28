# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, auth as auth_utils, database

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = auth_utils.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed_pw = auth_utils.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "Usuario creado"}

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = auth_utils.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    access_token = auth_utils.create_access_token({"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
