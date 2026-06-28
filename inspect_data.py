import kagglehub
import pandas as pd
import os

path = kagglehub.dataset_download("willianoliveiragibin/healthcare-insurance")
csv_file = os.path.join(path, "insurance.csv")

df = pd.read_csv(csv_file)

print("SHAPE:", df.shape)
print("\nTYPES:\n", df.dtypes)
print("\nFIRST 5 ROWS:\n", df.head())
print("\nMISSING VALUES:\n", df.isnull().sum())
print("\nDUPLICATES:", df.duplicated().sum())
print("\nSTATS:\n", df.describe())