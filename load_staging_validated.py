from connect import get_connection

# Our data-quality rules. A row is BAD if any of these are true:
#   - age outside a sane human range (0-120)
#   - charges null or negative (you can't be charged less than nothing)
#   - sex is empty/missing
# Everything else passes to STAGING.
REJECT_CONDITION = """
    age < 0 OR age > 120
    OR charges IS NULL OR charges < 0
    OR sex IS NULL OR TRIM(sex) = ''
"""

def load_staging_validated():
    conn = get_connection()
    cur = conn.cursor()

    # Idempotent reset of both destinations
    cur.execute("TRUNCATE TABLE HEALTHCARE_DE.STAGING.INSURANCE_STAGING")
    cur.execute("TRUNCATE TABLE HEALTHCARE_DE.QUARANTINE.INSURANCE_REJECTED")
    print("✅ STAGING + REJECTED emptied (idempotent reset)")

    # 1. GOOD ROWS → STAGING. Load only rows that do NOT match reject condition.
    cur.execute(f"""
        INSERT INTO HEALTHCARE_DE.STAGING.INSURANCE_STAGING
            (age, sex, bmi, children, smoker, region, charges)
        SELECT
            age, LOWER(TRIM(sex)), bmi, children,
            LOWER(TRIM(smoker)), LOWER(TRIM(region)), charges
        FROM HEALTHCARE_DE.RAW.INSURANCE_RAW
        WHERE NOT ({REJECT_CONDITION})
    """)
    good = cur.rowcount
    print(f"✅ Good rows → STAGING: {good}")

    # 2. BAD ROWS → REJECTED, each tagged with the reason it failed.
    #    A CASE expression assigns the specific reason.
    cur.execute(f"""
        INSERT INTO HEALTHCARE_DE.QUARANTINE.INSURANCE_REJECTED
            (age, sex, bmi, children, smoker, region, charges, reject_reason)
        SELECT
            age, sex, bmi, children, smoker, region, charges,
            CASE
                WHEN age < 0 OR age > 120          THEN 'invalid_age'
                WHEN charges IS NULL OR charges < 0 THEN 'invalid_charges'
                WHEN sex IS NULL OR TRIM(sex) = ''  THEN 'missing_sex'
                ELSE 'unknown'
            END AS reject_reason
        FROM HEALTHCARE_DE.RAW.INSURANCE_RAW
        WHERE {REJECT_CONDITION}
    """)
    bad = cur.rowcount
    print(f"✅ Bad rows → REJECTED: {bad}")

    # 3. THE REPORT — the interview-gold line.
    print(f"\n=== DATA QUALITY REPORT ===")
    print(f"   Total processed: {good + bad}")
    print(f"   Passed:          {good}")
    print(f"   Quarantined:     {bad}")
    print(f"   Pass rate:       {round(good / (good + bad) * 100, 2)}%")

    cur.close()
    conn.close()

if __name__ == "__main__":
    load_staging_validated()