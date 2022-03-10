from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from dag_etl.etl import run

DEFAULT_ARGS = {
    'owner':'krasko',
    'start_date':datetime(2022,3,10),
    'retries':2,
    'retry_delay':timedelta(minutes=15)
}


with DAG('data_from_api', default_args=DEFAULT_ARGS, schedule_interval='0 8 * * *') as dag:
    load_data = PythonOperator(
        task_id = 'load_task',
        python_callable=run,
	op_args = ['postgres_default', '{{ ds }}', '{{ next_ds }}']
    )
