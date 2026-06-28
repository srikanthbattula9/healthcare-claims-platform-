from connect import get_connection

def check_rejected():
    conn = get_connection()
    cur = conn.cursor()

    print("=== QUARANTINED ROWS ===")
    cur.execute("""
        SELECT age, sex, charges, reject_reason
        FROM HEALTHCARE_DE.QUARANTINE.INSURANCE_REJECTED
        ORDER BY reject_reason
    """)
    for r in cur.fetchall():
        print(f"   age={r[0]}, sex='{r[1]}', charges={r[2]}  →  {r[3]}")

    print("\n=== REJECT REASON SUMMARY ===")
    cur.execute("""
        SELECT reject_reason, COUNT(*)
        FROM HEALTHCARE_DE.QUARANTINE.INSURANCE_REJECTED
        GROUP BY reject_reason
        ORDER BY COUNT(*) DESC
    """)
    for r in cur.fetchall():
        print(f"   {r[0]}: {r[1]}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    check_rejected()