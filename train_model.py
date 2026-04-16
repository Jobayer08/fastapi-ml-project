import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# =========================
# Load Dataset
# =========================
df = pd.read_csv("data/bd_students_per_v2.csv")

# Drop useless columns
df = df.drop(columns=["id", "full_name"])

# =========================
# Split Features & Target
# =========================
X = df.drop("stu_group", axis=1)
y = df["stu_group"]

# Identify column types
categorical_cols = X.select_dtypes(include=["object"]).columns
numeric_cols = X.select_dtypes(exclude=["object"]).columns

# =========================
# Preprocessing
# =========================
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="mean"))
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_cols),
    ("cat", categorical_transformer, categorical_cols)
])

# =========================
# Pipeline
# =========================
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(random_state=42))
])

# =========================
# Train Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# Hyperparameter Tuning
# =========================
param_grid = {
    "model__n_estimators": [100, 200],
    "model__max_depth": [None, 10, 20],
    "model__min_samples_split": [2, 5]
}

grid = GridSearchCV(
    pipeline,
    param_grid,
    cv=3,
    scoring="accuracy",
    n_jobs=-1
)

# =========================
# Train
# =========================
grid.fit(X_train, y_train)

print("✅ Best Params:", grid.best_params_)
print(f"🎯 Best CV Accuracy: {grid.best_score_ * 100:.2f}%")

# =========================
# Test Accuracy
# =========================
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)

print(f"📊 Test Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# =========================
# Save Model
# =========================
joblib.dump(best_model, "model/student_model.pkl")

print("🚀 Model trained and saved successfully!")