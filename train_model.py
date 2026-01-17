import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

data = pd.DataFrame({
    "sugar": [5, 20, 1, 30, 10, 2, 15],
    "salt":  [0.2, 1.5, 0.1, 2.0, 0.5, 0.1, 0.9],
    "fat":   [1, 10, 0, 15, 3, 1, 7],
})

data["score"] = data["sugar"] + data["salt"] + data["fat"]
data["label"] = [2, 0, 2, 0, 1, 2, 1]

model = RandomForestClassifier()
model.fit(data[["sugar","salt","fat","score"]], data["label"])

pickle.dump(model, open("food_ai_model.pkl", "wb"))
print("Model saved!")

