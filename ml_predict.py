"""
ml_predict.py — predict charges for one new person.
Rebuilds the exact feature schema the model was trained on.
This module is what the FastAPI layer will import and call.
"""
import os
import pandas as pd
import joblib

ARTIFACTS = os.path.join(os.path.dirname(__file__), "ml_artifacts")

# The exact column order the model was trained on. The model is order-
# sensitive, so predictions MUST be built in this same layout.
FEATURE_COLUMNS = [
    "age", "sex", "smoker", "bmi", "children",
    "region_northeast", "region_northwest",
    "region_southeast", "region_southwest",
]

_model = None  # load once, reuse (lazy singleton)


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(f"{ARTIFACTS}/model.pkl")
    return _model


def predict_charge(person: dict) -> float:
    """
    person = {
        "age": 45, "sex": "male", "smoker": "yes",
        "bmi": 28.5, "children": 2, "region": "southwest"
    }
    Returns predicted charge in dollars.
    """
    # Start every feature at 0
    row = {col: 0 for col in FEATURE_COLUMNS}

    # Numeric features copy straight over
    row["age"] = person["age"]
    row["bmi"] = person["bmi"]
    row["children"] = person["children"]

    # Binary encodings — same rule as training
    row["sex"] = 1 if str(person["sex"]).lower() == "male" else 0
    row["smoker"] = 1 if str(person["smoker"]).lower() == "yes" else 0

    # One-hot the region: flip the matching region_* column to 1
    region_col = f"region_{str(person['region']).lower()}"
    if region_col in row:
        row[region_col] = 1
    else:
        raise ValueError(f"Unknown region: {person['region']}")

    # Build a 1-row DataFrame in the exact trained column order
    X = pd.DataFrame([row])[FEATURE_COLUMNS]

    prediction = get_model().predict(X)[0]
    return round(float(prediction), 2)


if __name__ == "__main__":
    # Two test people: a smoker and a non-smoker, otherwise identical
    smoker = {"age": 45, "sex": "male", "smoker": "yes",
              "bmi": 28.5, "children": 2, "region": "southwest"}
    nonsmoker = {**smoker, "smoker": "no"}

    print(f"Smoker     → ${predict_charge(smoker):,.2f}")
    print(f"Non-smoker → ${predict_charge(nonsmoker):,.2f}")
    print("(same person, only smoking differs — watch the gap)")
