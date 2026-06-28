from connect import get_connection

def setup_marts_layer():
    conn = get_connection()
    cur = conn.cursor()

    # MARTS schema — the gold layer, modeled for analytics
    cur.execute("CREATE SCHEMA IF NOT EXISTS HEALTHCARE_DE.MARTS")
    print("✅ MARTS schema ready")

    # DIMENSION table — one row per person, descriptive attributes.
    # person_id is the PRIMARY KEY (unique per person).
    cur.execute("""
        CREATE TABLE IF NOT EXISTS HEALTHCARE_DE.MARTS.DIM_PERSON (
            person_id  INTEGER,
            age        INTEGER,
            sex        STRING,
            smoker     STRING,
            region     STRING,
            bmi        FLOAT,
            children   INTEGER
        )
    """)
    print("✅ DIM_PERSON table ready")

    # FACT table — the measurement (charges), linked to the person
    # via person_id (FOREIGN KEY pointing back to DIM_PERSON).
    cur.execute("""
        CREATE TABLE IF NOT EXISTS HEALTHCARE_DE.MARTS.FACT_CHARGES (
            charge_id     INTEGER,
            person_id     INTEGER,
            charges       FLOAT,
            processed_at  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("✅ FACT_CHARGES table ready")

    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_marts_layer()