from pydantic import BaseModel, Field


# =========================
# USER SCHEMA
# =========================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=72)  # 🔥 bcrypt limit


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True   # SQLAlchemy support


# =========================
# STUDENT ML INPUT
# =========================

class StudentInput(BaseModel):
    study_hours: float = Field(..., ge=0, le=24)
    attendance: float = Field(..., ge=0, le=100)
    previous_score: float = Field(..., ge=0, le=100)


# =========================
# PREDICTION OUTPUT
# =========================

class PredictionOutput(BaseModel):
    prediction: str