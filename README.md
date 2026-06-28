# Healthcare Claims Intelligence Platform

An end-to-end data engineering pipeline that ingests healthcare insurance data,
processes it through a layered **medallion architecture**, and serves
analytics-ready insights via a dimensional **star schema** on Snowflake.

Built with Python and Snowflake, fully automated and version-controlled.

---

## Architecture

| Layer | Purpose |
|-------|---------|
| **RAW** | Immutable, exact copy of source data with audit timestamps. Never modified — guarantees replayability. |
| **STAGING** | Cleaned, standardized, deduplicated data. Idempotent truncate-and-load so re-runs never duplicate. |
| **MARTS** | Dimensional star schema (`FACT_CHARGES` + `DIM_PERSON`) modeled for analytics. |
| **VIEWS** | Business-ready analytics layer — region cost, smoker risk, age-band analysis. |

---

## Tech Stack

- **Database / Warehouse:** Snowflake
- **Language:** Python 3.14
- **Key libraries:** snowflake-connector-python, python-dotenv
- **Version control:** Git / GitHub
- **Architecture pattern:** Medallion (RAW → STAGING → MARTS), Star Schema

---

## Key Engineering Concepts Demonstrated

- **Medallion architecture** with strict layer separation
- **Idempotent loading** (truncate-and-load) — safe to re-run on a schedule
- **Dimensional modeling** — fact/dimension split, primary & foreign keys
- **Data validation** — row-count verification against source ("verify, don't trust")
- **Secrets management** — credentials isolated in `.env`, excluded from version control

---

## Pipeline Stages

| Script | What it does |
|--------|--------------|
| `connect.py` | Reusable Snowflake connection (credentials from `.env`) |
| `setup_raw.py` | Creates RAW schema + table |
| `load_raw.py` | Loads source data into RAW |
| `setup_staging.py` / `load_staging.py` | Builds + idempotently loads cleaned STAGING |
| `setup_marts.py` / `load_marts.py` | Builds star schema, splits data into fact + dimension |
| `setup_views.py` / `query_views.py` | Creates + queries analytics views |
| `check_*.py` | Validation scripts that verify each layer |

---

## Sample Insights

- Smokers incur **~3.8× higher** average charges than non-smokers ($32,050 vs $8,434)
- **Southeast** is the highest-cost region by average charge
- Average charges rise steadily with age — from ~$9,200 (under 30) to ~$21,200 (60+)

---

## Roadmap

- [ ] Data-quality framework (null checks, range validation, quarantine for bad records)
- [ ] Airflow orchestration with retries and monitoring
- [ ] PySpark transformations for large-scale processing
- [ ] ML layer — fraud/anomaly detection (scikit-learn + MLflow)
- [ ] CI/CD with GitHub Actions + Docker