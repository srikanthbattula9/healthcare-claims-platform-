import os
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("HealthcareParquet") \
    .master("local[*]") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("insurance_staging.csv", header=True, inferSchema=True)

# 1. WRITE AS PARQUET — plain, single output folder
df.write.mode("overwrite").parquet("output/insurance_parquet")
print("✅ Written as Parquet → output/insurance_parquet")

# 2. WRITE AS PARQUET, PARTITIONED BY region.
#    Spark physically splits the data into separate folders, one per region.
#    Queries that filter by region then read ONLY that folder (partition pruning).
df.write.mode("overwrite") \
    .partitionBy("region") \
    .parquet("output/insurance_by_region")
print("✅ Written as partitioned Parquet → output/insurance_by_region")

# 3. READ THE PARQUET BACK and prove it works (no inferSchema needed!)
print("\n=== Reading Parquet back ===")
pq = spark.read.parquet("output/insurance_parquet")
print(f"Row count: {pq.count()}")
pq.printSchema()   # schema came WITH the file — no guessing

spark.stop()