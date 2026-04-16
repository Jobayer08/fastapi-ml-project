from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import joblib

import database
import models
import schemas
import auth

# =============================
# APP INIT
# =============================

app = FastAPI(title="Student Group Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# LOAD MODEL
# =============================

model = joblib.load("model/student_model.pkl")

# =============================
# CREATE TABLES
# =============================

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)
    print("✅ Tables ready")

# =============================
# OAUTH
# =============================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
# ROOT
# =============================

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

# =============================
# REGISTER
# =============================

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username exists")

    hashed = auth.hash_password(user.password)
    new_user = models.User(username=user.username, password=hashed)

    db.add(new_user)
    db.commit()

    return {"message": "User registered"}

# =============================
# LOGIN
# =============================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token(data={"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}

# =============================
# VERIFY TOKEN
# =============================

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = auth.verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

# =============================
# PREDICT (REAL DATASET)
# =============================

@app.post("/predict")
def predict(
    data: schemas.StudentInput,
    username: str = Depends(get_current_user)
):
    # Convert input → DataFrame
    input_dict = data.dict()
    df = pd.DataFrame([input_dict])

    # Model prediction
    prediction = model.predict(df)[0]

    return {
        "username": username,
        "predicted_group": prediction
    }