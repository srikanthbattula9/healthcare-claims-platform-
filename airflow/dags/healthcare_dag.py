from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default settings applied to every task in this DAG
default_args = {
    "owner": "srikanth",
    "retries": 2,                          # retry a failed task twice
    "retry_delay": timedelta(minutes=1),   # wait 1 min between retries
}

# The DAG: a daily-scheduled healthcare pipeline
with DAG(
    dag_id="healthcare_pipeline",
    default_args=default_args,
    description="Medallion pipeline: RAW -> STAGING -> MARTS -> Views",
    schedule="@daily",                     # run once per day
    start_date=datetime(2026, 6, 1),
    catchup=False,                         # don't backfill past dates
    tags=["healthcare", "etl"],
) as dag:

    # Each task is a stage of your pipeline.
    # For now they're placeholder echo commands proving the structure;
    # next we wire them to your real Python scripts.
    setup_raw = BashOperator(
        task_id="setup_raw",
        bash_command="echo 'Setting up RAW layer'",
    )
    load_raw = BashOperator(
        task_id="load_raw",
        bash_command="echo 'Loading RAW'",
    )
    validate_stage = BashOperator(
        task_id="validate_and_load_staging",
        bash_command="echo 'Validating + loading STAGING'",
    )
    load_marts = BashOperator(
        task_id="load_marts",
        bash_command="echo 'Loading MARTS star schema'",
    )
    build_views = BashOperator(
        task_id="build_views",
        bash_command="echo 'Building analytics views'",
    )

    # THE DEPENDENCIES — this is the DAG. >> means "then".
    # This is your pipeline order, expressed as a graph.
    setup_raw >> load_raw >> validate_stage >> load_marts >> build_views