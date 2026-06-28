from connect import get_connection

def inject_bad_data():
    conn = get_connection()
    cur = conn.cursor()

    # Add deliberately broken rows to RAW to test our validation.
    # Each one violates a different rule:
    bad_rows = [
        (-5, 'male', 25.0, 0, 'no', 'southwest', 5000.0),      # negative age
        (200, 'female', 30.0, 1, 'yes', 'northeast', 8000.0),  # impossible age
        (35, 'male', 28.0, 2, 'no', 'southeast', -100.0),      # negative charges
        (40, 'female', 31.0, 1, 'yes', 'northwest', None),     # null charges
        (28, '', 26.0, 0, 'no', 'southeast', 4000.0),          # missing sex
    ]

    cur.executemany("""
        INSERT INTO HEALTHCARE_DE.RAW.INSURANCE_RAW
            (age, sex, bmi, children, smoker, region, charges)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, bad_rows)

    print(f"✅ Injected {len(bad_rows)} bad rows into RAW")

    cur.execute("SELECT COUNT(*) FROM HEALTHCARE_DE.RAW.INSURANCE_RAW")
    print(f"   RAW now has: {cur.fetchone()[0]} rows (was 1338)")

    cur.close()
    conn.close()

if __name__ == "__main__":
    inject_bad_data()