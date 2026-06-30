"""
ml_evaluate.py — test the model on the held-out set it never saw.
"""
import os
import pandas as pd
import joblib
from sklearn.metrics import r2_score, mean_absolute_error

ARTIFACTS = os.path.join(os.path.dirname(__file__), "ml_artifacts")


def main():
    model = joblib.load(f"{ARTIFACTS}/model.pkl")
    X_test = pd.read_pickle(f"{ARTIFACTS}/X_test.pkl")
    y_test = pd.read_pickle(f"{ARTIFACTS}/y_test.pkl")
    print(f"✅ Loaded model + {len(X_test)} unseen test rows")

    # Predict on data the model never trained on — the honest test
    predictions = model.predict(X_test)

    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    print(f"\n📊 R² score:  {r2:.3f}   (1.0 = perfect, explains variance)")
    print(f"📊 MAE:       ${mae:,.0f}   (avg dollars off per prediction)")

    # Show a few real-vs-predicted so the numbers feel concrete
    print("\nSample predictions (actual vs predicted):")
    for actual, pred in list(zip(y_test, predictions))[:5]:
        print(f"   actual ${actual:>10,.0f}   predicted ${pred:>10,.0f}")


if __name__ == "__main__":
    main()
