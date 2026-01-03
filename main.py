from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI(title="Student Performance Prediction API")

model = joblib.load("model/student_model.pkl")

class StudentData(BaseModel):
    study_hours: float
    attendance: float

@app.get("/")
def home():
    return {"message": "Student Prediction API Running"}

@app.post("/predict")
def predict(data: StudentData):
    prediction = model.predict([[data.study_hours, data.attendance]])
    
    result = "Pass" if prediction[0] == 1 else "Fail"
    
    return {
        "study_hours": data.study_hours,
        "attendance": data.attendance,
        "prediction": result
    }
