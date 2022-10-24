from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime

default_args = {
    'owner': 'admin',
    'start_date': datetime(2022, 10, 1),
    'end_date': datetime(2022, 10, 3),
}

dag_args = {
    'dag_id': 'file_sensor',
    'description': 'File Sensor DAG',
    'schedule_interval': '@daily',
    'default_args': default_args,
    'max_active_runs': 1,
}

with DAG(**dag_args) as dag:
    task_1 = BashOperator(
        task_id='create_file',
        # create a fili with the message "File sensor"
        bash_command='sleep 30 && echo "File sensor" > /tmp/file.txt',
    )
    
    task_2 = FileSensor(
        task_id='wait_for_file',
        filepath='/tmp/file.txt',
        poke_interval=5,
    )
    
    task_3 = BashOperator(
        task_id='print_file',
        bash_command='cat /tmp/file_sensor.txt',
    )
task_1 >> task_2 >> task_3