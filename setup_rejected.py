from connect import get_connection

def setup_rejected():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS HEALTHCARE_DE.QUARANTINE")

    # Same columns as source, PLUS a 'reject_reason' explaining the failure
    cur.execute("""
        CREATE TABLE IF NOT EXISTS HEALTHCARE_DE.QUARANTINE.INSURANCE_REJECTED (
            age            INTEGER,
            sex            STRING,
            bmi            FLOAT,
            children       INTEGER,
            smoker         STRING,
            region         STRING,
            charges        FLOAT,
            reject_reason  STRING,
            rejected_at    TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("✅ QUARANTINE.INSURANCE_REJECTED table ready")

    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_rejected()