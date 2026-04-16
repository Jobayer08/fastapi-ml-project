from pydantic import BaseModel, Field


# =========================
# USER SCHEMA (same as before)
# =========================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=72)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# =========================
# STUDENT ML INPUT (REAL DATASET)
# =========================

class StudentInput(BaseModel):
    age: int = Field(..., ge=10, le=25)
    gender: str
    location: str
    family_size: int = Field(..., ge=1, le=20)

    mother_education: str
    father_education: str
    mother_job: str
    father_job: str

    guardian: str
    parental_involvement: str
    internet_access: str

    studytime: int = Field(..., ge=0, le=24)
    tutoring: str
    school_type: str
    attendance: float = Field(..., ge=0, le=100)
    extra_curricular_activities: str

    english: float = Field(..., ge=0, le=100)
    math: float = Field(..., ge=0, le=100)
    science: float = Field(..., ge=0, le=100)
    social_science: float = Field(..., ge=0, le=100)
    art_culture: float = Field(..., ge=0, le=100)


# =========================
# PREDICTION OUTPUT
# =========================

class PredictionOutput(BaseModel):
    prediction: str