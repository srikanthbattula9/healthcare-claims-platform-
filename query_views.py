from connect import get_connection

def query_views():
    conn = get_connection()
    cur = conn.cursor()

    print("=== CHARGES BY REGION ===")
    cur.execute("SELECT * FROM HEALTHCARE_DE.MARTS.VW_CHARGES_BY_REGION")
    for r in cur.fetchall():
        print(f"   {r[0]:<12} | {r[1]} people | avg ${r[2]} | total ${r[3]}")

    print("\n=== SMOKER RISK ===")
    cur.execute("SELECT * FROM HEALTHCARE_DE.MARTS.VW_SMOKER_RISK")
    for r in cur.fetchall():
        print(f"   smoker={r[0]:<4} | {r[1]} people | avg ${r[2]}")

    print("\n=== CHARGES BY AGE BAND ===")
    cur.execute("SELECT * FROM HEALTHCARE_DE.MARTS.VW_CHARGES_BY_AGE_BAND")
    for r in cur.fetchall():
        print(f"   {r[0]:<6} | {r[1]} people | avg ${r[2]}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    query_views()