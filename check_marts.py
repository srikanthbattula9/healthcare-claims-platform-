from connect import get_connection

def check_marts():
    conn = get_connection()
    cur = conn.cursor()

    # 1. Row counts in both tables
    cur.execute("SELECT COUNT(*) FROM HEALTHCARE_DE.MARTS.DIM_PERSON")
    print(f"DIM_PERSON rows: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM HEALTHCARE_DE.MARTS.FACT_CHARGES")
    print(f"FACT_CHARGES rows: {cur.fetchone()[0]}")

    # 2. THE REAL TEST — join fact to dimension, compute avg charges by smoker.
    # You already know the answer: smokers pay ~4x more. If the join is
    # correct, that pattern MUST reappear. If the key linkage is broken,
    # the numbers will look wrong/scrambled.
    cur.execute("""
        SELECT
            d.smoker,
            COUNT(*)                       AS people,
            ROUND(AVG(f.charges), 2)       AS avg_charges
        FROM HEALTHCARE_DE.MARTS.FACT_CHARGES f
        JOIN HEALTHCARE_DE.MARTS.DIM_PERSON d
            ON f.person_id = d.person_id
        GROUP BY d.smoker
        ORDER BY avg_charges DESC
    """)
    print("\nAvg charges by smoker (joined across the star):")
    for row in cur.fetchall():
        print(f"   smoker={row[0]}  →  {row[1]} people, avg ${row[2]}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    check_marts()