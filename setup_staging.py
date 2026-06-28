from connect import get_connection

def setup_staging_layer():
    conn = get_connection()
    cur = conn.cursor()

    # STAGING schema — the silver layer, where data becomes trustworthy
    cur.execute("CREATE SCHEMA IF NOT EXISTS HEALTHCARE_DE.STAGING")
    print("✅ STAGING schema ready")

    # STAGING table — same columns, but note the additions:
    #   - processed_at: when this row was cleaned (audit trail, like loaded_at)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS HEALTHCARE_DE.STAGING.INSURANCE_STAGING (
            age           INTEGER,
            sex           STRING,
            bmi           FLOAT,
            children      INTEGER,
            smoker        STRING,
            region        STRING,
            charges       FLOAT,
            processed_at  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("✅ STAGING.INSURANCE_STAGING table ready")

    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_staging_layer()