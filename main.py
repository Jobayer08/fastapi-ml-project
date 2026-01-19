from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI(title="Student Exam Prediction API")

model = joblib.load("model/student_model.pkl")

class StudentInput(BaseModel):
    study_hours: float
    attendance: float
    previous_score: float

@app.get("/")
def root():
    return {"message": "Student Prediction API is running"}

@app.post("/predict")
def predict(data: StudentInput):
    prediction = model.predict([[
        data.study_hours,
        data.attendance,
        data.previous_score
    ]])

    return {
        "prediction": "Pass" if prediction[0] == 1 else "Fail"
    }
