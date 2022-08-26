# Creacion de un DAG para enviar datos de Google Cloud Storage a BigQuery

# Librerias de Airflow
from airflow import DAG
from airflow.utils.dates import days_ago

# Librerias Google Cloud Storage y BigQuery
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator


default_args = {
    'owner': 'admin',
    'start_date': days_ago(7)
}

dag_args = {
    'dag_id': 'send_data_storage_bigquery',
    'schedule_interval': '@daily',
    'catchup': False,
    'default_args': default_args
}

with DAG(**dag_args) as dag:
    
    gcs_to_bq = GCSToBigQueryOperator(
        task_id='cargar_datos_gcs_bq',
        bucket='main_buckets_airflow',
        source_objects=['*'],
        source_format='CSV',
        skip_leading_rows=1,
        field_delimiter=';',
        destination_project_dataset_table='noble-conduit-355722.working_dataset_airflow.retail_years',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_APPEND',
        gcp_conn_id='google_cloud_default2',
    )
    
    query = (
        '''
        SELECT 'year', 'area' ROUND(AVG('total_inc), 4) AS avg_income
        FROM 'noble-conduit-355722.working_dataset_airflow.retail_years'
        GROUP BY 'year', 'area'
        GROUP BY 'year', 'area'
        '''
    )
    
    tabla_resultados = BigQueryExecuteQueryOperator(
        task_id='tabla_resultados',
        sql=query,
        destination_dataset_table='noble-conduit-355722.working_dataset_airflow.retail_years_resultados',
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        use_legacy_sql=False,
        location='us-central1 ',
        gcp_conn_id='google_cloud_default2'
    )
    
    # Dependencias
    gcs_to_bq >> tabla_resultados

