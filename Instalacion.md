# Instalacion de Apache Airflow utilizando WSL y Anaconda

Que utilizamos para instalar Apache Airflow?

- [Anaconda](https://www.anaconda.com/)
- [WSL](https://docs.microsoft.com/en-us/windows/wsl/about)
- [Apache Airflow](https://airflow.apache.org/)
- [Visual Studio Code](https://code.visualstudio.com/)

Pasos para instalar Apache Airflow en WSL:

- Crear un env en Anaconda

        conda create --name airflow_env python=3.9 -y

- Creamos una carpeta llamada "airflow" en la carpeta de trabajo de nuestro proyecto.

        mkdir airflow

- Instanciamos AIRFLOW_HOME apuntando a la carpeta "airflow"

        export AIRFLOW_HOME=~/airflow 

        source ~/.bashrc

- Activar el env

        conda activate airflow_env

- Instalamos Apache Airflow

        pip install "apache-airflow==2.2.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-no-providers-3.9.txt"

- Ejecutamos Apache Airflow

        airflow db init

- Creamos el usuario airflow

        airflow users create \
            --username admin \
            --firstname <FirstName> \
            --lastname <LastName> \
            --role Admin \
            --email <YourEmail>

- Iniciamos Apache Airflow

        airflow webserver -D

        airflow scheduler -D

Ahora ya podemos ingresar a la aplicacion de Apache Airflow.

        http://localhost:8080