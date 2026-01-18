import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# -------------------------------
# TRAINING DATA (simple but solid)
# -------------------------------
# Each row = [sugar, salt, saturated_fat, score]
# class = 0 (unhealthy), 1 (moderate), 2 (healthy)

data = [
    [20, 2.0, 10, 32, 0],
    [15, 1.2, 8, 24, 0],
    [5, 0.3, 2, 7, 2],
    [8, 0.5, 3, 11, 2],
    [10, 0.8, 4, 14, 1],
    [12, 1.0, 6, 19, 1],
    [25, 2.5, 12, 39, 0],
    [30, 3.0, 15, 48, 0],
    [2, 0.1, 1, 3, 2],
    [7, 0.2, 2, 9, 2],
]

df = pd.DataFrame(data, columns=["sugar", "salt", "fat", "score", "label"])

X = df[["sugar", "salt", "fat", "score"]]
y = df["label"]

# -------------------------------
# TRAIN MODEL
# -------------------------------
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# -------------------------------
# SAVE MODEL
# -------------------------------
joblib.dump(model, "food_ai_model.pkl")

print("✅ New model trained and saved as food_ai_model.pkl")
