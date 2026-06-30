"""
ml_train.py — train a RandomForest to predict charges, save the model.
"""
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

ARTIFACTS = os.path.join(os.path.dirname(__file__), "ml_artifacts")


def main():
    # Load the SAME train split ml_prepare saved (never touch test here)
    X_train = pd.read_pickle(f"{ARTIFACTS}/X_train.pkl")
    y_train = pd.read_pickle(f"{ARTIFACTS}/y_train.pkl")
    print(f"✅ Loaded {len(X_train)} training rows")

    # n_estimators=100 → 100 trees voting. random_state=42 → reproducible.
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)   # <-- this is the actual "learning"
    print("✅ Model trained")

    # Persist the trained model so evaluate/predict can reuse it
    joblib.dump(model, f"{ARTIFACTS}/model.pkl")
    print(f"✅ Saved model to {ARTIFACTS}/model.pkl")

    # Bonus: which features mattered most? (great interview talking point)
    importances = sorted(
        zip(X_train.columns, model.feature_importances_),
        key=lambda x: x[1], reverse=True
    )
    print("\nFeature importance (what drives charges):")
    for name, score in importances:
        print(f"   {name:20s} {score:.3f}")


if __name__ == "__main__":
    main()
