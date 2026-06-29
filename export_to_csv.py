from connect import get_connection
import csv

def export_to_csv():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT age, sex, bmi, children, smoker, region, charges FROM HEALTHCARE_DE.STAGING.INSURANCE_STAGING")
    rows = cur.fetchall()

    # Write to a local CSV that Spark will read
    with open("insurance_staging.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["age", "sex", "bmi", "children", "smoker", "region", "charges"])  # header
        writer.writerows(rows)

    print(f"✅ Exported {len(rows)} rows to insurance_staging.csv")

    cur.close()
    conn.close()

if __name__ == "__main__":
    export_to_csv()