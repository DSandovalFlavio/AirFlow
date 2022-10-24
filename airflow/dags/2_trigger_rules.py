# DAG
from airflow import DAG
# PythonOperator
from airflow.operators.python import PythonOperator
# BashOperator
from airflow.operators.bash import BashOperator
# TriggerRule
from airflow.utils.trigger_rule import TriggerRule
# datetime
from datetime import datetime

def myfunction():
    return Exception

default_args = {
    'owner': 'admin',
    'start_date': datetime(2022, 1, 1),
    'end_date': datetime(2022, 10, 1),
    'depends_on_past': True,
}

dag_args = {
    'dag_id': 'trigger_rules',
    'schedule_interval': '@daily',
    'max_active_runs': 1, # Only one task instance can run at a time
    'default_args': default_args,
    'description': 'Trigger Rules DAG',
}

with DAG(**dag_args) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='sleep 5 && echo "Task 1"',
        trigger_rule=TriggerRule.ALL_SUCCESS,
        retries=3,
        retry_delay=5,
        depends_on_past=True,
    )
    
    task_2 = BashOperator(
        task_id='task_2',
        bash_command='sleep 3 && echo "Task 2"',
        trigger_rule=TriggerRule.ALL_SUCCESS,
        retries=3,
        retry_delay=5,
        depends_on_past=True,
    )
    
    task_3 = BashOperator(
        task_id='task_3',
        bash_command='sleep 2 && echo "Task 3"',
        trigger_rule=TriggerRule.ALWAYS,
        retries=2,
        retry_delay=15,
        depends_on_past=True,
    )
    
    task_4 = PythonOperator(
        task_id='task_4',
        python_callable=myfunction,
        retries=2,
        retry_delay=5,
        trigger_rule=TriggerRule.ALL_SUCCESS,
        depends_on_past=True,
    )
    
    task_5 = BashOperator(
        task_id='task_5',
        bash_command='sleep 2 && echo "Task 5"',
        retries=2,
        retry_delay=15,
        depends_on_past=True,
    )
    
task_1 >> task_2 >> task_3 >> task_4 >> task_5