from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.extract import extract
from scripts.load import load
from scripts.transform import transform

default_args = {
    "owner": "ashish",
    "start_date": datetime(2026, 4, 2),
    "retries": 1
}
with DAG(
        dag_id = "s3_incremental_pipeline",
        default_args = default_args,
        schedule_interval = "@daily",
        catchup = False) as dag:
    extract_task = PythonOperator(
            task_id = "extract",python_callable = extract
            )
    load_task = PythonOperator(
            task_id = "load", python_callable = load)
    transform_task = PythonOperator(
            task_id = "transform",python_callable = transform)
    extract_task >> transform_task >> load_task
