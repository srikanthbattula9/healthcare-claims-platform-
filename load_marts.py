from connect import get_connection

def load_marts():
    conn = get_connection()
    cur = conn.cursor()

    # Idempotent: empty both tables first (same pattern you proved earlier)
    cur.execute("TRUNCATE TABLE HEALTHCARE_DE.MARTS.DIM_PERSON")
    cur.execute("TRUNCATE TABLE HEALTHCARE_DE.MARTS.FACT_CHARGES")
    print("✅ MARTS tables emptied (idempotent reset)")

    # LOAD DIM_PERSON — descriptive attributes, one row per person.
    # ROW_NUMBER() generates a unique person_id (the primary key) since
    # the source has no id. This is a window function — your SQL muscle.
    cur.execute("""
        INSERT INTO HEALTHCARE_DE.MARTS.DIM_PERSON
            (person_id, age, sex, smoker, region, bmi, children)
        SELECT
            ROW_NUMBER() OVER (ORDER BY age, sex, region)  AS person_id,
            age, sex, smoker, region, bmi, children
        FROM HEALTHCARE_DE.STAGING.INSURANCE_STAGING
    """)
    print(f"✅ DIM_PERSON loaded: {cur.rowcount} rows")

    # LOAD FACT_CHARGES — the measurement, linked to person via person_id.
    # We re-derive the SAME person_id with the SAME ordering so the fact
    # rows line up with the matching dimension rows (the foreign key link).
    cur.execute("""
        INSERT INTO HEALTHCARE_DE.MARTS.FACT_CHARGES
            (charge_id, person_id, charges)
        SELECT
            ROW_NUMBER() OVER (ORDER BY age, sex, region)  AS charge_id,
            ROW_NUMBER() OVER (ORDER BY age, sex, region)  AS person_id,
            charges
        FROM HEALTHCARE_DE.STAGING.INSURANCE_STAGING
    """)
    print(f"✅ FACT_CHARGES loaded: {cur.rowcount} rows")

    cur.close()
    conn.close()

if __name__ == "__main__":
    load_marts()