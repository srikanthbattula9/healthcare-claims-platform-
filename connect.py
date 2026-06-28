import os
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()

def get_connection():
    """Open a connection to Snowflake using credentials from .env"""
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM insurance")
    result = cur.fetchone()
    print(f"✅ Connected. Row count from Python: {result[0]}")
    cur.close()
    conn.close()