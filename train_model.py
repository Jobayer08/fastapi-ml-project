import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

df = pd.read_csv("data/student_data.csv")

X = df[["study_hours", "attendance", "previous_score"]]
y = df["result"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("model", RandomForestClassifier(random_state=42))
])

param_grid = {
    "model__n_estimators": [100, 200, 300],
    "model__max_depth": [None, 4, 6, 8],
    "model__min_samples_split": [2, 5, 10]
}

grid = GridSearchCV(
    pipeline,
    param_grid,
    cv=3,
    scoring="accuracy",
    n_jobs=-1
)

grid.fit(X_train, y_train)

print("✅ Best Params:", grid.best_params_)
print(f"🎯 Best CV Accuracy: {grid.best_score_ * 100:.2f}%")

best_model = grid.best_estimator_

y_pred = best_model.predict(X_test)
print(f"📊 Test Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

joblib.dump(best_model, "model/student_model.pkl")
