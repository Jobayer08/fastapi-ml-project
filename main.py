from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import database
import models
import schemas
import auth

import joblib


# =============================
# APP INIT
# =============================

app = FastAPI(
    title="Student Exam Prediction API with JWT and Database"
)


# Create tables
models.Base.metadata.create_all(
    bind=database.engine
)


# Load ML model
model = joblib.load(
    "model/student_model.pkl"
)


# OAuth
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# =============================
# DATABASE DEPENDENCY
# =============================

def get_db():

    db = database.SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =============================
# ROOT API
# =============================

@app.get("/")
def root():

    return {
        "message":
        "API running with JWT + Database"
    }


# =============================
# REGISTER API
# =============================

@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # Check existing user

    existing_user = db.query(
        models.User
    ).filter(
        models.User.username == user.username
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    # Hash password

    hashed_password = auth.hash_password(
        user.password
    )


    # Create user

    new_user = models.User(

        username=user.username,

        password=hashed_password

    )


    db.add(new_user)

    db.commit()

    return {

        "message":
        "User registered successfully"

    }


# =============================
# LOGIN API
# =============================

@app.post("/login")
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    user = db.query(
        models.User
    ).filter(
        models.User.username ==
        form_data.username
    ).first()


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )


    if not auth.verify_password(
        form_data.password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )


    access_token = auth.create_access_token(

        data={
            "sub": user.username
        }

    )


    return {

        "access_token":
        access_token,

        "token_type":
        "bearer"

    }


# =============================
# VERIFY TOKEN
# =============================

def get_current_user(

    token: str = Depends(oauth2_scheme)

):

    username = auth.verify_token(token)

    if username is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return username


# =============================
# INPUT SCHEMA
# =============================

@app.post("/predict")
def predict(

    data: schemas.StudentInput,

    username: str =
    Depends(get_current_user)

):

    prediction = model.predict([[

        data.study_hours,

        data.attendance,

        data.previous_score

    ]])


    result = "Pass" if prediction[0] == 1 else "Fail"


    return {

        "username": username,

        "prediction": result,

        "study_hours": data.study_hours,

        "attendance": data.attendance,

        "previous_score": data.previous_score

    }