from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='bronze_ingestion_dag',
    default_args=default_args,
    description='Ingestão de dados da Open Brewery API para S3 (camada bronze)',
    schedule_interval='@daily',
    catchup=False,
    tags=['bronze', 'inbev'],
) as dag:

    ingest_brewery_data = BashOperator(
        task_id='run_bronze_ingest_script',
        bash_command='python /opt/airflow/scripts/bronze_ingest.py',
    )

    ingest_brewery_data
