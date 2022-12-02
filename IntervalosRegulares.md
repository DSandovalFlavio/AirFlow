# Intervalos Regulares

Los DAGs pueden ser ejecutados en intervalos regulares, por ejemplo cada 5 minutos, cada hora, cada dia, etc.

Por ejemplo:

Si quisieramos programar la ejecucion de un DAG que extraiga datos de una base de datos y tambien extraiga informacion de una API, y que estos datos se almacenen en un archivo CSV, podriamos programar el DAG para que se ejecute cada dia.

```python

# Defininimos los argumentos del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1)
}

dag_args = {
# ***** Aqui es donde definimos el intervalo de ejecucion del DAG *****
    'schedule_interval': '@daily', 
# *******************************************************************
    'default_args': default_args
}

with DAG('example_dag', **dag_args) as dag:

    # Definimos el Task que ejecuta la extraccion de datos de la base de datos
    extract_data = BashOperator(
        task_id='extract_data',
        bash_command='python extract_data.py'
    )

    # Definimos el Task que ejecuta la extraccion de datos de la API
    extract_api = BashOperator(
        task_id='extract_api',
        bash_command='python extract_api.py'
    )

    # Definimos el Task que ejecuta la extraccion de datos de la API
    save_data = BashOperator(
        task_id='save_data',
        bash_command='python save_data.py'
    )

    # Definimos la dependencia entre los Task
    extract_data >> extract_api >> save_data

```

Airflow nos proporciona una serie de intervalos regulares que podemos usar para programar la ejecucion de un DAG, estos son:

- @once: Solo se ejecuta una vez
- @hourly: Se ejecuta cada hora
- @daily: Se ejecuta cada dia
- @weekly: Se ejecuta cada semana
- @monthly: Se ejecuta cada mes
- @yearly: Se ejecuta cada año

Documentacion: https://airflow.apache.org/docs/apache-airflow/1.10.1/scheduler.html

Airflow utiliza `start_date` y `schedule_interval` para calcular la fecha y hora de la siguiente ejecucion del DAG.

Por ejemplo, si definimos un DAG con `start_date` en `2018-01-01` y `schedule_interval` en `@daily`, el se ejecutara por primera vez exactamente a las 00:00:00 del 2018-01-01, y luego se ejecutara cada dia a las 00:00:00.

Si estamos en la fecha 2018-01-01 a las 12:00:00 y queremos ejecutar el DAG, tendremos que hacerlo manualmente, ya que su proxima ejecucion sera a las 00:00:00 del 2018-01-02.

![intervalos regulares](imag/intervalos%20regulares.png)

Tambien podemos poner fin a la fecha de ejecucion de un DAG, para esto debemos definir `end_date` en el DAG.

