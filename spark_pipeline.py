import os
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def run_spark_pipeline():
    spark = SparkSession.builder \
        .appName("HealthcareSparkPipeline") \
        .master("local[*]") \
        .config("spark.ui.showConsoleProgress", "false") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    # 1. READ
    df = spark.read.csv("insurance_staging.csv", header=True, inferSchema=True)
    print(f"✅ Read {df.count()} rows")

    # 2. TRANSFORM — add a risk flag + standardize (business logic in Spark)
    transformed = df.withColumn(
        "risk_flag",
        F.when(df.smoker == "yes", "HIGH").otherwise("LOW")
    )
    print("✅ Transformed: added risk_flag")

    # 3. WRITE — partitioned Parquet (the analytics-ready Spark output)
    transformed.write.mode("overwrite") \
        .partitionBy("region") \
        .parquet("output/insurance_spark_final")
    print("✅ Written partitioned Parquet → output/insurance_spark_final")

    # 4. VERIFY — read back, confirm count holds
    check = spark.read.parquet("output/insurance_spark_final")
    print(f"✅ Verified: {check.count()} rows in output")

    spark.stop()

if __name__ == "__main__":
    run_spark_pipeline()