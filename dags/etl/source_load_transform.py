from datetime import datetime, timedelta
from textwrap import dedent
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


with DAG(
    "extract_load_flatten",
    default_args={
        "depends_on_past": False,
        "email": ["aditya.nikhil.patel@gmail.com"],
        "email_on_failure": True,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    },
    description="Polls betting websites and flattens data",
    schedule=timedelta(days=1),
    start_date=datetime(2023, 3, 1),
    catchup=False,
    tags=["Extract-Load-Flatten"],
) as dag:

    t1 = DummyOperator(
        task_id="fetch_data",
    )

    t2 = BashOperator(
        task_id="run_pipeline_data",
        bash_command="cd /dbt && dbt run --models flattened --profiles-dir ."
    )

    t1 >> t2