# Create Custom Operator

from airflow import DAG
from datetime import datetime
from hellooperator import HelloOperator

default_args = {
    'owner': 'admin',
    'start_date': datetime(2022, 10, 1),
}

dag_args = {
    'dag_id': 'custom_operator',
    'schedule_interval': '@once',
    'catchup': False,
    'default_args': default_args,
    'description': 'Custom Operator DAG',
}

with DAG(**dag_args) as dag:
    hello_task = HelloOperator(task_id='hello_task', name='Airflow')
