from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Verb, UserProgress, ExamResult
from app.api import auth, verbs, practice, admin

app = FastAPI(
    title="French Verbs Trainer",
    description="Entrena tus verbos en francés",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(verbs.router)
app.include_router(practice.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "¡Bienvenido al Entrenador de Verbos en Francés! 🇫🇷"}
