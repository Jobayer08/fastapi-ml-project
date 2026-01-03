import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# Sample dataset
data = {
    "study_hours": [1,2,3,4,5,6,7,8],
    "attendance": [40,45,50,60,65,70,80,90],
    "result": [0,0,0,0,1,1,1,1]  # 0 = Fail, 1 = Pass
}

df = pd.DataFrame(data)

X = df[["study_hours", "attendance"]]
y = df["result"]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "model/student_model.pkl")

print("✅ Model trained and saved")
