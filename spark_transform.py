import os
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"

from pyspark.sql import SparkSession
from pyspark.sql import functions as F   # Spark's function library

spark = SparkSession.builder \
    .appName("HealthcareTransform") \
    .master("local[*]") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("insurance_staging.csv", header=True, inferSchema=True)

# 1. FILTER — only smokers (like SQL: WHERE smoker = 'yes')
print("=== Smokers only (first 5) ===")
df.filter(df.smoker == "yes").show(5)

# 2. GROUP BY + AGGREGATE — avg charges by smoker
#    (like SQL: SELECT smoker, AVG(charges) GROUP BY smoker)
print("=== Avg charges by smoker ===")
df.groupBy("smoker") \
  .agg(
      F.count("*").alias("people"),
      F.round(F.avg("charges"), 2).alias("avg_charges")
  ) \
  .orderBy(F.desc("avg_charges")) \
  .show()

# 3. SELECT + new column — add a 'risk_flag' (like SQL CASE)
print("=== With risk flag ===")
df.withColumn(
    "risk_flag",
    F.when(df.smoker == "yes", "HIGH").otherwise("LOW")
).select("age", "smoker", "charges", "risk_flag").show(5)

spark.stop()