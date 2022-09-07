import datetime as dt
from pathlib import Path
import pandas as pd

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# def default arguments
default_args = {
    'owner': 'admin',
    'start_date': dt.datetime(2019, 1, 1),
}

dag_args = {
    'dag_id': 'dag_no_programado',
    'schedule_interval': None,
    'default_args': default_args,
}

with DAG(**dag_args) as dag:
    
    fetch_events = BashOperator(
        task_id="fetch_events",
        bash_command=(
            "mkdir -p /data/events && "
            "curl -o /data/events.json http://events_api:5000/events"
        )
    )
    
    def _calculate_stats(input_path, output_path):
        Path(output_path).parent.mkdir(exist_ok=True)
        events = pd.read_json(input_path)
        stats = events.groupby(["date", "user"]).size().reset_index()
        stats.to_csv(output_path, index=False)
    
    calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={"input_path": "/data/events.json", "output_path": "/data/stats.csv"}
    )
    
fetch_events >> calculate_stats