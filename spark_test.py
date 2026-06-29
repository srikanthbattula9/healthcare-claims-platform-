from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HealthcareTest") \
    .master("local[*]") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()

# Quiet Spark's logging — only show real errors
spark.sparkContext.setLogLevel("ERROR")

print("✅ Spark session created!")
print(f"   Spark version: {spark.version}")

data = [("alice", 30), ("bob", 45), ("carol", 28)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()

spark.stop()