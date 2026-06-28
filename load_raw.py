from connect import get_connection

def load_raw():
    conn = get_connection()
    cur = conn.cursor()

    # Copy every row from the source table into RAW.
    # We select only the 7 source columns — loaded_at fills itself
    # automatically via the DEFAULT CURRENT_TIMESTAMP() we set up.
    cur.execute("""
        INSERT INTO HEALTHCARE_DE.RAW.INSURANCE_RAW
            (age, sex, bmi, children, smoker, region, charges)
        SELECT age, sex, bmi, children, smoker, region, charges
        FROM HEALTHCARE_DE.CLAIMS.INSURANCE
    """)
    print(f"✅ Rows loaded into RAW: {cur.rowcount}")

    # Verify: count what's actually in RAW now
    cur.execute("SELECT COUNT(*) FROM HEALTHCARE_DE.RAW.INSURANCE_RAW")
    print(f"✅ RAW row count confirmed: {cur.fetchone()[0]}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    load_raw()