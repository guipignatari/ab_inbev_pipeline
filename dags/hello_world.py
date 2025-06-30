from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

with DAG(
    dag_id="hello_world",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["teste"]
) as dag:
    start = DummyOperator(task_id="start")
