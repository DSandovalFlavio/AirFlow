from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'admin',
    'start_date': datetime(2022, 10, 1),
    'end_date': datetime(2022, 10, 3),
}

dag_args = {
    'dag_id': 'external_task_sensor',
    'description': 'External Task Sensor DAG',
    'schedule_interval': '@daily',
    'default_args': default_args,
}

with DAG(**dag_args) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='sleep 10 && echo "DAG finalizado"',
        depends_on_past=True
    )
    
task_1