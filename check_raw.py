from connect import get_connection

def check_raw():
    conn = get_connection()
    cur = conn.cursor()

    # How many rows are really in RAW?
    cur.execute("SELECT COUNT(*) FROM HEALTHCARE_DE.RAW.INSURANCE_RAW")
    print(f"Total rows in RAW: {cur.fetchone()[0]}")

    # How many distinct load timestamps? Each full load = one timestamp batch.
    # If you loaded twice, you'll see TWO different loaded_at values.
    cur.execute("""
        SELECT loaded_at, COUNT(*) 
        FROM HEALTHCARE_DE.RAW.INSURANCE_RAW
        GROUP BY loaded_at
        ORDER BY loaded_at
    """)
    print("Rows per load batch (loaded_at, count):")
    for row in cur.fetchall():
        print(f"   {row[0]}  →  {row[1]} rows")

    cur.close()
    conn.close()

if __name__ == "__main__":
    check_raw()