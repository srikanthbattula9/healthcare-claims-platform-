import os
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HealthcarePruning") \
    .master("local[*]") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Read the PARTITIONED parquet
df = spark.read.parquet("output/insurance_by_region")

# Query filtering on region — Spark should prune to just one partition
southeast = df.filter(df.region == "southeast")
print(f"Southeast rows: {southeast.count()}")

# .explain() shows Spark's PHYSICAL PLAN — proof of what it actually reads.
# Look for "PartitionFilters" in the output — that's pruning in action.
print("\n=== Spark's execution plan (look for PartitionFilters) ===")
southeast.explain()

spark.stop()