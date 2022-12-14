# Que es un DAG?

![Imagen del DAG](/imag/DagsGrafo.png)

Como se aprecia un DAG es una estructura de datos que permite la ejecución de una serie de tareas en orden por lo que tambien podemos llamarles pipelines de datos.

Los pipelines de datos generalmente consisten en varias tareas o acciones que deben ejecutarsepara lograr el resultado deseado.

La unidad principal con la que Airflow define un flujo de trabajo es el Grafo Acíclico Dirigido (DAG). Los nodos del grafo son las diferentes tareas y las aristas dirigidas muestran las relaciones y dependencias entre ellas. La propiedad acíclica permite que el DAG sea ejecutado de principio a fin sin entrar en ningún bucle.

![Imagen del DAG](/imag/dag3.png)

Una buena propiedad de esta representacion del DAG es que propociona un algoritmo relativamente sencillo que podemos usar para ejecutar nuestro pipeline de datos.

Ejemplo de secuencia de un DAG:

- Para cada tarea abierta o incompleta haga lo siguiente

  - Para cada arista apuntando hacia la tarea, verifique si la tarea upstream se ha completado.
  - Si se ha completado la tarea upstream, agregue la tarea actual a la cola de tareas pendientes de ejecución.

- Ejecute las tareas en la cola de ejecucion, marcandolas como completadas una vez que se han ejecutado.
- Repita el proceso hasta que todas las tareas sean completadas.

![Imagen del DAG](/imag/flujodag.png)

Hasta ahora hemos vista que al representar un DAG podemos dividirlo en una serie de tareas, esto nos permite dividir el flujo de trabajo en una serie de pasos que podemos ejecutar de forma independiente o en paralelo dependiendo el caso, de esta forma obtenemos una gran flexibilidad y un mejor performance.

## Estructura de un DAG en codigo:

### Argumentos:

Son valores que son pasados a un DAG para que se apliquen a cualquier operador.

```python
default_args = {
    'owner': 'dsandovalflavio', # Propietario del DAG
    'start_date': days_ago(2),  # Fecha de inicio del DAG
    'sla' : timedelta(hours=3) # Tiempo de tolerancia para la ejecucion del DAG
}
```

### Task:

Un Task define una unidad de trabajo dentro de un DAG.
Es representado como un nodo en la vista del DAG.
Esta escrito en python, donde cada Task es una implementacion de un Operator.

```python
simple_task = BashOperator(
    task_id='simple_task', # Nombre del Task
    depends_on_past=False, # Si el Task depende del anterior
    bash_command='echo "Hello World"', # Comando a ejecutar
    sla=timedelta(hours=3), # Tiempo de tolerancia para la ejecucion del Task
    dag=dag, # DAG al que pertenece el Task, si usamos with DAG no es necesario
    default_args=default_args # Argumentos por defecto del DAG
)
```

Al estarse ejecutando un DAG, cada Task se ejecuta de forma independiente y estos task pueden tener un estado representado en la ui como los siguientes

![Imagen del DAG](/imag/estadostask.png)

- success: Tarea completada con exito
- running: Tarea en ejecucion
- failed: Tarea fallida
- skipped: Tarea omitida
- rescheduled: Tarea re-planeada
- retry: Tarea re-intentada
- queued: Tarea en cola de ejecucion
- no status: Tarea no ejecutada

### Operadores

Los Operadores son las clases que implementan la funcionalidad de una tarea.
Y existen varios tipos de Operadores por ejemplo:

- BashOperator: Ejecuta un comando bash
- PythonOperator: Ejecuta una funcion python
- DummyOperator: Ejecuta una funcion python sin ejecutar

A su ves los operadores se pueden clasificar en:

- Action Operators: Son Operadores que ejecutan una accion, por ejemplo una tarea que ejecuta un comando bash.

- Transfer Operators: Son Operadores que ejecutan una transferencia de archivos, por ejemplo:

  - AzureFileTransferOperator
  - FacebookAdsTransferOperator
  - PrestoTransferOperator

- Sensor Operators: Son Operadores que ejecutan un sensor, por ejemplo:

  - HdfsSensorOperator
  - HivePartitionSensorOperator
  - TimeSensorOperator

### Dependencias

En la representacion del DAG existen dependencias entre tareas, estas se representan como aristas dirigidas.

```python
start >> section_1 >> section_2 >> end
```

![Imagen del DAG](/imag/dependencias.png)

## Funcionamiento

Cuando se ejecuta un DAG, se ejecutan las tareas en orden, es decir, se ejecuta la tarea upstream y luego la tarea downstream.
Para que este proceso se ejecute de forma correcta Airflow se apoya de sus 3 componentes principales:

- **Scheduler**: Analiza los DAGs , verifica su intervalo de programacion y ( si la programacion de los DAGs ha pasado) comienza a programar las tareas de los DAGs para su ejecucion pasandolas a los Workers.
- **Workers**: Son los encargados de recolectar las tareas programadas por el Scheduler y ejecutarlas. Se podria decir que los Workers son los responsables de realizar el trabajo.
-  **Airflow Webserver**: Es el encargado de mostrar la informacion de los DAGs y sus tareas en la UI.

![Imagen del DAG](/imag/Funcionamiento.png)

### Monitorizacion

El webserver de Airflow nos da informacion detallada de los procesos y como se ejecutan dentro de su UI.
![Imagen del DAG](/imag/informacion_airflow.png)