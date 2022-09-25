# Creando mi primer DAG

# Librerias de Airflow
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Funciones de Python
from datetime import date
from random import random

# Definir el DAG

# Definimos los argumentos por defecto del DAG
default_args = {
    'owner': 'admin', # Propietario del DAG
    'start_date': days_ago(2), # Fecha de inicio del DAG
}

# Definimos el DAG
dag_args = {
    'dag_id': 'mi_primer_dag', # Identificador del DAG
    'schedule_interval': '@daily',   # Intervalo de ejecucion del DAG
    'catchup': False,           # Evitar ejecuciones atrasadas
    'default_args': default_args, # Argumentos por defecto del DAG
}

# Para evitar redundancia, se utiliza el context manager with
with DAG(**dag_args) as dag:
    
    # Definimos la primera tarea con una tarea Bash
    bash_task = BashOperator(
        task_id='bash_task', # Identificador de la tarea
        bash_command='echo "--> Mi primer DAG con Apache Airflow!, Fecha: $TODAY"', # Comando a ejecutar
        env={'TODAY': str(date.today())}, # Variables de entorno
    )
    
    # Creamos una funcion en Python para la segunda tarea
    def print_random(number=None, otro=None):
        for i in range(number):
            print(f'--> Numero aleatorio: {i+1}', random())
            
    # Definimos la segunda tarea con una tarea Python
    python_task = PythonOperator(
        task_id='python_task', # Identificador de la tarea
        python_callable=print_random, # Funcion a ejecutar
        op_kwargs={'number': 10}, # Argumentos de la funcion
    )
    
# Definimos la dependencia entre las tareas
bash_task >> python_task # Dependencia entre las tareas

