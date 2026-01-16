import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# -------------------------------------------------------
# Create better training data (4 features)
# sugar, salt, sat_fat, palm_oil, label
# -------------------------------------------------------

data = [
    [2, 0.1, 0.2, 0, "healthy"],
    [5, 0.3, 1.0, 0, "healthy"],
    [8, 0.6, 2.0, 1, "moderate"],
    [12, 0.8, 3.5, 1, "moderate"],
    [18, 1.2, 5.0, 1, "unhealthy"],
    [30, 1.5, 8.0, 1, "unhealthy"],
    [40, 2.0, 10.0, 1, "very unhealthy"],
]

columns = ["sugar", "salt", "sat_fat", "palm_oil", "label"]
df = pd.DataFrame(data, columns=columns)

# -------------------------------------------------------
# Split training data
# -------------------------------------------------------

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------------------------------
# Train model
# -------------------------------------------------------

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# -------------------------------------------------------
# Save the model
# -------------------------------------------------------

joblib.dump(model, "food_ai_model.pkl")

print("✔ Model trained and saved (with palm_oil feature).")
