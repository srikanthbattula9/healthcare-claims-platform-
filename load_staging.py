from connect import get_connection

def load_staging():
    conn = get_connection()
    cur = conn.cursor()

    # STEP 1 — TRUNCATE: empty STAGING first. This is what makes the load
    # idempotent. Run it once or 100 times, you always start from empty,
    # so you can never accumulate duplicates. Safe because STAGING is
    # rebuildable from RAW (the rule you nailed earlier).
    cur.execute("TRUNCATE TABLE HEALTHCARE_DE.STAGING.INSURANCE_STAGING")
    print("✅ STAGING emptied (idempotent reset)")

    # STEP 2 — CLEAN + LOAD: pull from RAW, standardize as we go.
    #   - LOWER(TRIM(...)) on text: fixes 'Male', ' male ', 'MALE' -> 'male'
    #   - We select only the 7 data columns; processed_at fills itself.
    cur.execute("""
        INSERT INTO HEALTHCARE_DE.STAGING.INSURANCE_STAGING
            (age, sex, bmi, children, smoker, region, charges)
        SELECT
            age,
            LOWER(TRIM(sex))      AS sex,
            bmi,
            children,
            LOWER(TRIM(smoker))   AS smoker,
            LOWER(TRIM(region))   AS region,
            charges
        FROM HEALTHCARE_DE.RAW.INSURANCE_RAW
    """)
    print(f"✅ Rows cleaned and loaded into STAGING: {cur.rowcount}")

    # STEP 3 — VERIFY: count what landed (verify-don't-trust)
    cur.execute("SELECT COUNT(*) FROM HEALTHCARE_DE.STAGING.INSURANCE_STAGING")
    print(f"✅ STAGING row count confirmed: {cur.fetchone()[0]}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    load_staging()