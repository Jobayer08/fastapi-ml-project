from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
import joblib
import auth

# =============================
# App initialize
# =============================

app = FastAPI(title="Student Exam Prediction API with JWT Auth")

# Load ML model
model = joblib.load("model/student_model.pkl")

# JWT settings (same as auth.py)
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =============================
# Root API
# =============================

@app.get("/")
def root():
    return {"message": "Student Prediction API is running with JWT Authentication"}


# =============================
# Login API
# =============================

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = auth.authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = auth.create_access_token(
        data={"sub": user}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =============================
# Verify JWT Token
# =============================

def verify_token(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# =============================
# Input Schema
# =============================

class StudentInput(BaseModel):

    study_hours: float
    attendance: float
    previous_score: float


# =============================
# Protected Prediction API
# =============================

@app.post("/predict")
def predict(
    data: StudentInput,
    username: str = Depends(verify_token)
):

    prediction = model.predict([[
        data.study_hours,
        data.attendance,
        data.previous_score
    ]])

    result = "Pass" if prediction[0] == 1 else "Fail"

    return {

        "username": username,
        "study_hours": data.study_hours,
        "attendance": data.attendance,
        "previous_score": data.previous_score,
        "prediction": result

    }
