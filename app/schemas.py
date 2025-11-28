from pydantic import BaseModel

# =====================
# Auth
# =====================
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# =====================
# Verbos
# =====================
class VerbCreate(BaseModel):
    spanish: str
    infinitive: str
    presente_je: str
    presente_tu: str
    presente_il: str
    presente_nous: str
    presente_vous: str
    presente_ils: str
    passe_compose: str

class VerbOut(BaseModel):
    id: int
    spanish: str
    infinitive: str

    class Config:
        from_attributes = True

# Alias por compatibilidad
VerbResponse = VerbOut

# =====================
# Progreso de usuario
# =====================
class UserProgressOut(BaseModel):
    id: int
    user_id: int
    verb_id: int
    total_attempts: int
    correct_attempts: int

    class Config:
        from_attributes = True

# =====================
# Resultado de examen
# =====================
class ExamResultOut(BaseModel):
    id: int
    user_id: int
    score: int
    total: int
    timestamp: str

    class Config:
        from_attributes = True

# =====================
# Práctica individual
# =====================
class PresenteAnswers(BaseModel):
    je: str
    tu: str
    il: str
    nous: str
    vous: str
    ils: str

class PasseAnswers(BaseModel):
    je: str

class IndividualPracticeRequest(BaseModel):
    verb_id: int
    presente: PresenteAnswers
    passe: PasseAnswers
