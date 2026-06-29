import os
# Point Spark at Java 17 (Spark-compatible), not the system Java 25
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HealthcareSpark") \
    .master("local[*]") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("insurance_staging.csv", header=True, inferSchema=True)

print("✅ Data loaded into Spark\n")
print(f"Row count: {df.count()}")
print("\nSchema (Spark's inferred types):")
df.printSchema()
print("First 5 rows:")
df.show(5)

spark.stop()