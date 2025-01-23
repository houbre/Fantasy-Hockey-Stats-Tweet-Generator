from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os


def run_script():
    os.system('python ETL.py -p HelloThere')


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 22), 
    'retries': 1,
}

dag = DAG(
    'post_fantasy_stats_to_twitter',
    default_args=default_args,
    description='A DAG to post fantasy stats to Twitter at 3 AM every day',
    schedule_interval='0 3 * * *',  # Run at 3 AM daily
    catchup=False,
)

post_to_twitter_task = PythonOperator(
    task_id='post_to_twitter',
    python_callable=run_script,
    dag=dag,
)
