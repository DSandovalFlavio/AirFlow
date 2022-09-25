import json
import pathlib
import airflow
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'admin',
    'start_date': days_ago(14),
}

dag_args = {
    'dag_id': 'download_rocket_launches',
    'schedule_interval': None,
    'default_args': default_args,
}

with DAG(**dag_args) as dag:
    
    download_launches = BashOperator(
        task_id="download_launches",
        bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    )
    
    print_launches = BashOperator(
        task_id="print_launches",
        bash_command="cat /tmp/launches.json",
    )

    def _get_launches():
        pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)
        
        with open("/tmp/launches.json") as f:
            launches = json.load(f)
            image_urls = [launch["image"] for launch in launches["results"]]
            print(image_urls)
            for image_url in image_urls:
                try:
                    response = requests.get(image_url)
                    image_filename = image_url.split("/")[-1]
                    target_file = f"/tmp/images/{image_filename}"
                    with open(target_file, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded {image_url} to {target_file}.")
                except requests_exceptions.MissingSchema:
                    print(f"Invalid URL {image_url}")
                except requests_exceptions.ConnectionError:
                    print(f"Failed to get {image_url}")
                    
    get_launches = PythonOperator(
        task_id="get_launches",
        python_callable=_get_launches,
    )

    notify = BashOperator(
        task_id="notify",
        bash_command='echo "There are now $(ls /tmp/images | wc -l) images."',
    )

download_launches >> print_launches >> get_launches >> notify
    
    