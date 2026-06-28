from connect import get_connection

def check_staging():
    conn = get_connection()
    cur = conn.cursor()

    # 1. Row count
    cur.execute("SELECT COUNT(*) FROM HEALTHCARE_DE.STAGING.INSURANCE_STAGING")
    print(f"Total rows in STAGING: {cur.fetchone()[0]}")

    # 2. Check distinct values in cleaned columns — should be tidy & consistent
    for col in ["sex", "smoker", "region"]:
        cur.execute(f"""
            SELECT {col}, COUNT(*) 
            FROM HEALTHCARE_DE.STAGING.INSURANCE_STAGING
            GROUP BY {col}
            ORDER BY {col}
        """)
        print(f"\nDistinct '{col}' values:")
        for row in cur.fetchall():
            print(f"   {row[0]}  →  {row[1]} rows")

    cur.close()
    conn.close()

if __name__ == "__main__":
    check_staging()