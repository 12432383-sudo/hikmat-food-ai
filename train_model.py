import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# -----------------------------------
# Step 1: Create training data
# -----------------------------------

data = [
    # sugar, salt, sat_fat, palm_oil, label
    [2, 0.1, 0.2, 0, 0],   # healthy
    [5, 0.3, 1.0, 0, 0],   # healthy
    [8, 0.6, 2.0, 0, 1],   # moderate
    [12, 0.8, 3.5, 1, 1],  # moderate
    [20, 1.2, 6.0, 1, 2],  # unhealthy
    [30, 1.5, 8.0, 1, 2],  # unhealthy
    [40, 2.0, 10.0, 1, 2]  # very unhealthy
]

columns = ["sugar", "salt", "sat_fat", "palm_oil", "label"]
df = pd.DataFrame(data, columns=columns)

# -----------------------------------
# Step 2: Split data
# -----------------------------------

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------------
# Step 3: Train model
# -----------------------------------

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -----------------------------------
# Step 4: Save model
# -----------------------------------

joblib.dump(model, "food_ai_model.pkl")

print("✅ Model trained and saved as food_ai_model.pkl")
