from connect import get_connection

def setup_views():
    conn = get_connection()
    cur = conn.cursor()

    # VIEW 1 — Charges by region. The classic "where is cost highest?" question.
    cur.execute("""
        CREATE OR REPLACE VIEW HEALTHCARE_DE.MARTS.VW_CHARGES_BY_REGION AS
        SELECT
            d.region,
            COUNT(*)                  AS people,
            ROUND(AVG(f.charges), 2)  AS avg_charges,
            ROUND(SUM(f.charges), 2)  AS total_charges
        FROM HEALTHCARE_DE.MARTS.FACT_CHARGES f
        JOIN HEALTHCARE_DE.MARTS.DIM_PERSON d ON f.person_id = d.person_id
        GROUP BY d.region
        ORDER BY avg_charges DESC
    """)
    print("✅ VW_CHARGES_BY_REGION ready")

    # VIEW 2 — Smoker risk: avg charges split by smoker status.
    cur.execute("""
        CREATE OR REPLACE VIEW HEALTHCARE_DE.MARTS.VW_SMOKER_RISK AS
        SELECT
            d.smoker,
            COUNT(*)                  AS people,
            ROUND(AVG(f.charges), 2)  AS avg_charges
        FROM HEALTHCARE_DE.MARTS.FACT_CHARGES f
        JOIN HEALTHCARE_DE.MARTS.DIM_PERSON d ON f.person_id = d.person_id
        GROUP BY d.smoker
        ORDER BY avg_charges DESC
    """)
    print("✅ VW_SMOKER_RISK ready")

    # VIEW 3 — Age-band analysis using CASE to bucket ages into groups.
    # This is where 'age as a dimension' (bucketed) comes alive.
    cur.execute("""
        CREATE OR REPLACE VIEW HEALTHCARE_DE.MARTS.VW_CHARGES_BY_AGE_BAND AS
        SELECT
            CASE
                WHEN d.age < 30 THEN '18-29'
                WHEN d.age < 45 THEN '30-44'
                WHEN d.age < 60 THEN '45-59'
                ELSE '60+'
            END                        AS age_band,
            COUNT(*)                   AS people,
            ROUND(AVG(f.charges), 2)   AS avg_charges
        FROM HEALTHCARE_DE.MARTS.FACT_CHARGES f
        JOIN HEALTHCARE_DE.MARTS.DIM_PERSON d ON f.person_id = d.person_id
        GROUP BY age_band
        ORDER BY age_band
    """)
    print("✅ VW_CHARGES_BY_AGE_BAND ready")

    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_views()