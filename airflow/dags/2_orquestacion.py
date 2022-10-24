from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'admin',
    'start_date': datetime(2022, 9, 1),
    'end_date': datetime(2022, 10, 1),
    'depends_on_past': True, # Hace que la tarea se ejecute solo si la tarea anterior se ejecutó con éxito.
}

dag_args = {
    'dag_id': 'orquestacion',
    'schedule_interval': '@daily',
    'default_args': default_args,
    'description': 'Orquestacion DAG',
}

with DAG(**dag_args) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='sleep 2 && echo "Task 1"'
    )
    
    task_2 = BashOperator(
        task_id='task_2',
        bash_command='sleep 2 && echo "Task 2"'
    )
    
    task_3 = BashOperator(
        task_id='task_3',
        bash_command='sleep 2 && echo "Task 3"'
    )
    
    task_4 = BashOperator(
        task_id='task_4',
        bash_command='sleep 2 && echo "Task 4"'
    )
    
task_1 >> task_2 >> [task_3, task_4]