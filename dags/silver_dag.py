from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 6, 30),
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
    'email': ['guilherme.pignatari@icloud.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG(
    dag_id="silver_transform_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="Transforma dados da camada bronze e salva como Parquet na camada silver",
) as dag:

    run_silver_transform = BashOperator(
        task_id="run_silver_transform_script",
        bash_command="python /opt/airflow/scripts/silver_transform.py",
        env={
            "AWS_ACCESS_KEY_ID": "{{ var.value.AWS_ACCESS_KEY_ID }}",
            "AWS_SECRET_ACCESS_KEY": "{{ var.value.AWS_SECRET_ACCESS_KEY }}",
            "AWS_DEFAULT_REGION": "{{ var.value.AWS_DEFAULT_REGION }}",
            "S3_BUCKET": "{{ var.value.S3_BUCKET }}",
        },
    )

    run_silver_transform
