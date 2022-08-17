# Que es un DAG?

![Imagen del DAG](/imag/DagsGrafo.png)

Como se aprecia un DAG es una estructura de datos que permite la ejecución de una serie de tareas en orden por lo que tambien podemos llamarles pipelines de datos.

Los pipelines de datos generalmente consisten en varias tareas o acciones que deben ejecutarsepara lograr el resultado deseado.

La unidad principal con la que Airflow define un flujo de trabajo es el Grafo Acíclico Dirigido (DAG). Los nodos del grafo son las diferentes tareas y las aristas dirigidas muestran las relaciones y dependencias entre ellas. La propiedad acíclica permite que el DAG sea ejecutado de principio a fin sin entrar en ningún bucle.
