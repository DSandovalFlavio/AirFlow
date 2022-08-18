# Creacion de un DAG para enviar datos de Google Cloud Storage a BigQuery

# Librerias de Airflow
from airflow import DAG
from airflow.utils.dates import days_ago

# Librerias Google Cloud Storage y BigQuery
from google.providers.cloud.transfers.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from google.providers.cloud.operators.bigquery import BigQueryExecuteQueryOperator

default_args = {
    'owner': 'admin',
    'start_date': days_ago(7),
}

dag_args = {
    'dag_id': 'send_data_storage_bigquery',
    'schedule_interval': '@daily',
    'catchup': False,
    default_args: default_args
}

with DAG(**dag_args) as dag:
    
    gcs_to_bq = GoogleCloudStorageToBigQueryOperator(
        task_id='cargar_datos_gcs_bq',
        bucket='main_buckets_airflow',
        source_objects=['*'],
        source_format='CSV',
        skip_leading_rows=1,
        field_delimiter=';',
        destination_project_dataset_table='noble-conduit-355722.working_dataset_airflow.retail_data',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_APPEND',
        bigquery_conn_id='google_cloud_default',
        google_cloud_storage_conn_id='google_cloud_default',
    )
    bq_query = BigQueryExecuteQueryOperator(
        task_id='bq_query',
        sql='{{ var.value.sql }}',
        destination_dataset_table='{{ var.value.destination_dataset_table }}',
        write_disposition='WRITE_TRUNCATE',
        dag=dag
    )
    gcs_to_bq >> bq_query

