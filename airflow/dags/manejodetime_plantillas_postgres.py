# """
# Documentation of pageview format: https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Pageviews
# """

# airflow dependencies
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

# other dependencies
from urllib import request

# default arguments
default_args = {
    'owner': 'admin',
    'start_date': days_ago(1),
}

# dag arguments
dag_args = {
    'dag_id': 'ETL_wikipedia_pageviews_to_postgres',
    'schedule_interval': '@hourly',
    'default_args': default_args,
    'template_searchpath': '/tmp',
    'max_active_runs': 1,
}

# dag
with DAG(**dag_args) as dag:

    # def function to get pageviews
    def _get_data(year, month, day, hour, output_path):
        url = (
            "https://dumps.wikimedia.org/other/pageviews/"
            f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
        )
        print(f'Month: {month:0>2}, {month}')
        request.urlretrieve(url, output_path)

    # task to get pageviews
    get_data = PythonOperator(
        task_id="get_data",
        python_callable=_get_data,
        op_kwargs={
            "year": "{{ execution_date.year }}",
            "month": "{{ execution_date.month }}",
            "day": "{{ execution_date.day }}",
            "hour": "{{ execution_date.hour }}",
            "output_path": "/tmp/wikipageviews.gz",
        }
    )

    # task to unzip pageviews
    extract_gz = BashOperator(
        task_id="extract_gz", 
        bash_command="gunzip --force /tmp/wikipageviews.gz"
    )

    # task to create sql script to load pageviews
    def _fetch_pageviews(pagenames, execution_date):
        result = dict.fromkeys(pagenames, 0)
        # read file
        with open("/tmp/wikipageviews", "r") as f:
            for line in f:
                domain_code, page_title, view_counts, _ = line.split(" ")
                if domain_code == "en" and page_title in pagenames:
                    result[page_title] = view_counts
        # write file sql
        with open("/tmp/postgres_query.sql", "w") as f:
            for pagename, pageviewcount in result.items():
                f.write(
                    "INSERT INTO pageview_counts VALUES ("
                    f"'{pagename}', {pageviewcount}, '{execution_date}'"
                    ");\n"
                )

    # task to create sql script to load pageviews
    fetch_pageviews = PythonOperator(
        task_id="fetch_pageviews",
        python_callable=_fetch_pageviews,
        op_kwargs={"pagenames": {"Google", "Amazon", "Apple", "Microsoft", "Facebook"}}
    )

    # task to load pageviews to postgres
    write_to_postgres = PostgresOperator(
        task_id="write_to_postgres",
        postgres_conn_id="my_postgres",
        sql="postgres_query.sql"
    )

get_data >> extract_gz >> fetch_pageviews >> write_to_postgres
