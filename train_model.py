import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Load data
df = pd.read_csv("data/student_data.csv")

X = df[["study_hours", "attendance", "previous_score"]]
y = df["result"]

# Pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression())
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
pipeline.fit(X_train, y_train)

# Accuracy
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Save full pipeline
joblib.dump(pipeline, "model/student_model.pkl")

print("✅ Model trained with preprocessing")
print(f"🎯 Accuracy: {accuracy * 100:.2f}%")
