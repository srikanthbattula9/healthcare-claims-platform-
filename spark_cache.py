import os
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import time

spark = SparkSession.builder \
    .appName("HealthcareCache") \
    .master("local[*]") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("insurance_staging.csv", header=True, inferSchema=True)

# A filtered DataFrame we'll reuse several times — a caching candidate
smokers = df.filter(df.smoker == "yes")

# --- WITHOUT cache: each action recomputes the filter from scratch ---
start = time.time()
print(f"Smoker count: {smokers.count()}")
print(f"Avg smoker charges: {smokers.agg(F.avg('charges')).collect()[0][0]:.2f}")
print(f"Max smoker charges: {smokers.agg(F.max('charges')).collect()[0][0]:.2f}")
print(f"⏱  Without cache: {time.time() - start:.3f}s\n")

# --- WITH cache: compute once, reuse from memory ---
smokers.cache()              # mark for caching
smokers.count()              # first action triggers the cache to populate

start = time.time()
print(f"Smoker count: {smokers.count()}")
print(f"Avg smoker charges: {smokers.agg(F.avg('charges')).collect()[0][0]:.2f}")
print(f"Max smoker charges: {smokers.agg(F.max('charges')).collect()[0][0]:.2f}")
print(f"⏱  With cache: {time.time() - start:.3f}s")

spark.stop()