from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime

default_args = {
    'owner': 'admin',
    'start_date': datetime(2022, 10, 1),
    'end_date': datetime(2022, 10, 3),
}

dag_args = {
    'dag_id': 'external_task_sensor_resep',
    'description': 'External Task Sensor DAG Reseptor',
    'schedule_interval': '@daily',
    'default_args': default_args,
}

with DAG(**dag_args) as dag:
    task_1 = ExternalTaskSensor(
        task_id='wait_for_dag',
        external_dag_id='external_task_sensor',
        external_task_id='task_1',
        poke_interval=5,
    )
    
    task_2 = BashOperator(
        task_id='task_2_after_task_1',
        bash_command='sleep 10 && echo "DAG completed for wait_for_dag"',
        depends_on_past=True
    )
    
task_1 >> task_2