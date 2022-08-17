# Introduccion a Apache AirFlow

Estos apuntes estan desarrollados en Python 3.9 y Apache Airflow 2.2.3.

### ¿Que es Apache Airflow?

Apache Airflow es un framework para automatizar la ejecucion de tareas de una forma sencilla y eficiente creando canalizaciones de datos programadas utilizando un marco flexible en python, y al mismo tiempo proporciona muchos componentes basicos que le permiten unir las muchas tecnologias diferentes que actualmente se encuentran en la ingenieria de datos.

Podriamos considerar a Airflow como un intermediario que controla y coordina el trabajo que se lleva a cabo en los diferentes sistemas.
Airflow no es una herramienta de procesamiento de datos en si misma, sino que orquesta los diferentes componentes responsables de procesar sus datos en canalizaciones de datos.


Es dessarrollado en Airbnb en 2014 y en 2016 se tranfiere ala fundacion Apache.

## Puntos clave sobre Airflow:

- Apache Airflow es una plataforma Open Source para programar y monitorear workflow de datos.
- Esta desarrollado en Python por lo que es 100% personalizable.
- Es actualmente utilizado por cientos de empresas en todo el mundo.

## Las caracteristicas de Apache Airflow son:

- Dinamico: Los pipelines son creados apartir de codigo y esto nos da mucha flexibilidad.
- Elegante: Los pipelines son creados de forma explicita y sencilla.
- Extensible: Apache Airflow es extensible y se puede agregar nuevas funcionalidades.
- Escalable: Ya que tiene una arquitectura modular.

## Conceptos alrededor de Airflow:

- Pipeline: Una secuencia de tareas que se ejecutan en orden.
- Workflow: Conjunto de elementos que sirven para procesar datos, de forma no lineal.
- ETL: Es el proceso de Extraction, Transformation y Load.

## Componentes de Airflow:

- Web Server: se encarga de proveer la interfaz gráfica donde el usuario puede interactuar con los flujos de trabajo y revisar el estado de las tareas que los componen. 

- Scheduler: es el componente encargado de planificar las ejecuciones de las tareas y las pipelines definidas por el usuario. Cuando las tareas están listas para ser ejecutadas, estas son enviadas al Executor. 

- Executor: define cómo las tareas van a ser ejecutadas y son enviadas a los Workers. Airflow proporciona diferentes tipos de Executors que pueden ejecutar las tareas de manera secuencial (SequentialExecutor) o permitiendo la paralelización de las mismas (LocalExecutor, CeleryExecutor, etc.). 

- Worker: es el proceso o subproceso que ejecuta las tareas. Dependiendo de la configuración del Executor, habrá uno o varios Workers que reciban diferentes tareas. 

- Metastore: es una base de datos donde se guardan todos los metadatos de Airflow y de los flujos de trabajo definidos. Es utilizado por el Scheduler, el Executor y el Webserver para guardar sus estados.

![Imagen de la arquitectura de Apache Airflow](/imag/componentes_airflow.png)

## Explorando UI de Apache Airflow

Al iniciar el programa se muestra la pantalla de inicio de Apache Airflow, donde se pueden ver la lista de DAGs y sus estados.

![Imagen de la interfaz de Apache Airflow](/imag/ui_airflow.png)

En la seccion de segurity obtendremos una lista de usuarios y roles que pueden acceder a la aplicación, ademas de algunas estadisticas de uso de la aplicación.

![Seccion segurity](/imag/segurity.png)