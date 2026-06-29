from connect import get_connection

def load_raw():
    conn = get_connection()
    cur = conn.cursor()

    # Empty RAW first so re-running can't create duplicates (idempotent)
    cur.execute("TRUNCATE TABLE HEALTHCARE_DE.RAW.INSURANCE_RAW")

    # Copy every row from the source table into RAW.
    cur.execute("""
        INSERT INTO HEALTHCARE_DE.RAW.INSURANCE_RAW
            (age, sex, bmi, children, smoker, region, charges)
        SELECT age, sex, bmi, children, smoker, region, charges
        FROM HEALTHCARE_DE.CLAIMS.INSURANCE
    """)
    print(f"✅ Rows loaded into RAW: {cur.rowcount}")

    cur.execute("SELECT COUNT(*) FROM HEALTHCARE_DE.RAW.INSURANCE_RAW")
    print(f"✅ RAW row count confirmed: {cur.fetchone()[0]}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    load_raw()