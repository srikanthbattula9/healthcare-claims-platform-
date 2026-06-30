"""
ml_prepare.py — pull MARTS data, encode categoricals, train/test split.
"""
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from connect import get_connection

ARTIFACTS = os.path.join(os.path.dirname(__file__), "ml_artifacts")
os.makedirs(ARTIFACTS, exist_ok=True)


def load_dataframe():
    conn = get_connection()
    query = """
        SELECT d.age, d.sex, d.smoker, d.region, d.bmi, d.children,
               f.charges
        FROM HEALTHCARE_DE.MARTS.DIM_PERSON d
        JOIN HEALTHCARE_DE.MARTS.FACT_CHARGES f
          ON d.person_id = f.person_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df.columns = [c.lower() for c in df.columns]
    return df


def encode(df):
    df["smoker"] = (df["smoker"].str.lower() == "yes").astype(int)
    df["sex"] = (df["sex"].str.lower() == "male").astype(int)
    df = pd.get_dummies(df, columns=["region"], prefix="region")
    return df


def main():
    df = load_dataframe()
    print(f"✅ Pulled {len(df)} rows from MARTS")

    df = encode(df)
    print(f"✅ Encoded. Columns now: {list(df.columns)}")

    X = df.drop(columns=["charges"])
    y = df["charges"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"✅ Split: {len(X_train)} train rows, {len(X_test)} test rows")

    X_train.to_pickle(f"{ARTIFACTS}/X_train.pkl")
    X_test.to_pickle(f"{ARTIFACTS}/X_test.pkl")
    y_train.to_pickle(f"{ARTIFACTS}/y_train.pkl")
    y_test.to_pickle(f"{ARTIFACTS}/y_test.pkl")
    print(f"✅ Saved train/test artifacts to {ARTIFACTS}/")


if __name__ == "__main__":
    main()
