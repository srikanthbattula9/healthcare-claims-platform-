from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "srikanth",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

# All scripts live in the mounted project dir. We cd there first so that
# `from connect import get_connection` resolves and load_dotenv() finds .env.
PROJECT = "/opt/airflow/project"

with DAG(
    dag_id="healthcare_pipeline",
    default_args=default_args,
    description="Medallion pipeline: RAW -> STAGING -> MARTS -> Views",
    schedule="@daily",
    start_date=datetime(2026, 6, 1),
    catchup=False,
    tags=["healthcare", "etl"],
) as dag:

    setup_raw = BashOperator(
        task_id="setup_raw",
        bash_command=f"cd {PROJECT} && python setup_raw.py",
    )

    load_raw = BashOperator(
        task_id="load_raw",
        bash_command=f"cd {PROJECT} && python load_raw.py",
    )

    # Staging stage: build staging table + quarantine table, then validated load
    validate_stage = BashOperator(
        task_id="validate_and_load_staging",
        bash_command=(
            f"cd {PROJECT} && python setup_staging.py "
            f"&& python setup_rejected.py "
            f"&& python load_staging_validated.py"
        ),
    )

    load_marts = BashOperator(
        task_id="load_marts",
        bash_command=f"cd {PROJECT} && python setup_marts.py && python load_marts.py",
    )

    build_views = BashOperator(
        task_id="build_views",
        bash_command=f"cd {PROJECT} && python setup_views.py",
    )

    setup_raw >> load_raw >> validate_stage >> load_marts >> build_views