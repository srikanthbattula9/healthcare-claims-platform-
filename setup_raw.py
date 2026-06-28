from connect import get_connection  # reuse the connection we already built

def setup_raw_layer():
    conn = get_connection()
    cur = conn.cursor()

    # 1. Create the RAW schema — our bronze landing zone, separate from CLAIMS
    cur.execute("CREATE SCHEMA IF NOT EXISTS HEALTHCARE_DE.RAW")
    print("✅ RAW schema ready")

    # 2. Create the RAW table — same columns as source, PLUS an audit timestamp
    cur.execute("""
        CREATE TABLE IF NOT EXISTS HEALTHCARE_DE.RAW.INSURANCE_RAW (
            age        INTEGER,
            sex        STRING,
            bmi        FLOAT,
            children   INTEGER,
            smoker     STRING,
            region     STRING,
            charges    FLOAT,
            loaded_at  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("✅ RAW.INSURANCE_RAW table ready")

    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_raw_layer()