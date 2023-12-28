# Keepcoding-Devops-Liberando-productos
# Practica final - Albert Fernández

## Objetivo

El objetivo es mejorar un proyecto creado previamente para ponerlo en producción, a través de la adicción de una serie de mejoras.

## Proyecto inicial

El proyecto inicial es un servidor que realiza lo siguiente:

- Utiliza [FastAPI](https://fastapi.tiangolo.com/) para levantar un servidor en el puerto `8081` e implementa inicialmente dos endpoints:
  - `/`: Devuelve en formato `JSON` como respuesta `{"message":"Hello World"}` y un status code 200.
  - `/health`: Devuelve en formato `JSON` como respuesta`{"health": "ok"}` y un status code 200.

- Se han implementado tests unitarios para el servidor [FastAPI](https://fastapi.tiangolo.com/)

- Utiliza [prometheus-client](https://github.com/prometheus/client_python) para arrancar un servidor de métricas en el puerto `8000` y poder registrar métricas, siendo inicialmente las siguientes:
  - `Counter('server_requests_total', 'Total number of requests to this webserver')`: Contador que se incrementará cada vez que se haga una llamada a alguno de los endpoints implementados por el servidor (inicialmente `/` y `/health`)
  - `Counter('healthcheck_requests_total', 'Total number of requests to healthcheck')`: Contador que se incrementará cada vez que se haga una llamada al endpoint `/health`.
  - `Counter('main_requests_total', 'Total number of requests to main endpoint')`: Contador que se incrementará cada vez que se haga una llamada al endpoint `/`.

## Software necesario

Es necesario disponer del siguiente software:

- `Python` en versión `3.8.5` o superior, disponible para los diferentes sistemas operativos en la [página oficial de descargas](https://www.python.org/downloads/release/python-385/)

- `virtualenv` para poder instalar las librerías necesarias de Python, se puede instalar a través del siguiente comando:

    ```sh
    pip3 install virtualenv
    ```

    En caso de estar utilizando Linux y el comando anterior diera fallos se debe ejecutar el siguiente comando:

    ```sh
    sudo apt-get update && sudo apt-get install -y python3.8-venv
    ```

- `Docker` para poder arrancar el servidor implementado a través de un contenedor Docker, es posible descargarlo a [través de su página oficial](https://docs.docker.com/get-docker/).

## Ejecución de servidor

### Ejecución directa con Python

1. Instalación de un virtualenv, **realizarlo sólo en caso de no haberlo realizado previamente**:
   1. Obtener la versión actual de Python instalada para crear posteriormente un virtualenv:

        ```sh
        python3 --version
        ```

        El comando anterior mostrará algo como lo mostrado a continuación:ç

        ```sh
            Python 3.8.13
        ```

   2. Crear de virtualenv en la raíz del directorio para poder instalar las librerías necesarias:

       - En caso de en el comando anterior haber obtenido `Python 3.8.*`

            ```sh
            python3.8 -m venv venv
            ```

       - En caso de en el comando anterior haber obtenido `Python 3.9.*`:

           ```sh
           python3.9 -m venv venv
           ```

2. Activar el virtualenv creado en el directorio `venv` en el paso anterior:

     ```sh
     source venv/bin/activate
     ```

3. Instalar las librerías necesarias de Python, recogidas en el fichero `requirements.txt`, **sólo en caso de no haber realizado este paso previamente**. Es posible instalarlas a través del siguiente comando:

    ```sh
    pip3 install -r requirements.txt
    ```

4. Ejecución del código para arrancar el servidor:

    ```sh
    python3 src/app.py
    ```

5. La ejecución del comando anterior debería mostrar algo como lo siguiente:

    ```sh
    [2022-04-16 09:44:22 +0000] [1] [INFO] Running on http://0.0.0.0:8081 (CTRL + C to quit)
    ```

### Ejecución a través de un contenedor Docker

1. Crear una imagen Docker con el código necesario para arrancar el servidor:

    ```sh
    docker build -t simple-server:0.0.1 .
    ```

2. Arrancar la imagen construida en el paso anterior mapeando los puertos utilizados por el servidor de FastAPI y el cliente de prometheus:

    ```sh
    docker run -d -p 8000:8000 -p 8081:8081 --name simple-server simple-server:0.0.1
    ```

3. Obtener los logs del contenedor creado en el paso anterior:

    ```sh
    docker logs -f simple-server
    ```

4. La ejecución del comando anterior debería mostrar algo como lo siguiente:

    ```sh
    [2022-04-16 09:44:22 +0000] [1] [INFO] Running on http://0.0.0.0:8081 (CTRL + C to quit)
    ```

## Comprobación de endpoints de servidor y métricas

Una vez arrancado el servidor, utilizando cualquier de las formas expuestas en los apartados anteriores, es posible probar las funcionalidades implementadas por el servidor:

- Comprobación de servidor FastAPI, a través de llamadas a los diferentes endpoints:

  - Realizar una petición al endpoint `/`

      ```sh
      curl -X 'GET' \
      'http://0.0.0.0:8081/' \
      -H 'accept: application/json'
      ```

      Debería devolver la siguiente respuesta:

      ```json
      {"message":"Hello World"}
      ```

  - Realizar una petición al endpoint `/health`

      ```sh
      curl -X 'GET' \
      'http://0.0.0.0:8081/health' \
      -H 'accept: application/json' -v
      ```

      Debería devolver la siguiente respuesta.

      ```json
      {"health": "ok"}
      ```

- Comprobación de registro de métricas, si se accede a la URL `http://0.0.0.0:8000` se podrán ver todas las métricas con los valores actuales en ese momento:

  - Realizar varias llamadas al endpoint `/` y ver como el contador utilizado para registrar las llamadas a ese endpoint, `main_requests_total` ha aumentado, se debería ver algo como lo mostrado a continuación:

    ```sh
    # TYPE main_requests_total counter
    main_requests_total 4.0
    ```

  - Realizar varias llamadas al endpoint `/health` y ver como el contador utilizado para registrar las llamadas a ese endpoint, `healthcheck_requests_total` ha aumentado, se debería ver algo como lo mostrado a continuación:

    ```sh
    # TYPE healthcheck_requests_total counter
    healthcheck_requests_total 26.0
    ```

  - También se ha credo un contador para el número total de llamadas al servidor `server_requests_total`, por lo que este valor debería ser la suma de los dos anteriores, tal y como se puede ver a continuación:

    ```sh
    # TYPE server_requests_total counter
    server_requests_total 30.0
    ```

## Tests

Se ha implementado tests unitarios para probar el servidor FastAPI, estos están disponibles en el archivo `src/tests/app_test.py`.

Es posible ejecutar los tests de diferentes formas:

- Ejecución de todos los tests:

    ```sh
    pytest
    ```

- Ejecución de todos los tests y mostrar cobertura:

    ```sh
    pytest --cov
    ```

- Ejecución de todos los tests y generación de report de cobertura:

    ```sh
    pytest --cov --cov-report=html
    ```

## Practica a realizar

### Comprobamos que todo el entorno funcione correctamente:
1. Activamos el entorno virtual, en este caso al estar en windows usamos el script:
    ```sh
     source venv/Scripts/activate
    ```
2. Instalamos las dependencias y requerimientos dentro del venv:
    ```sh
     pip3 install -r requirements.txt
    ```

3. Ejecutamos con Python y accedemos vía localhost a los endpoints de la app:
    ```sh
     python src/app.py
    ```
    ![Endpoints](Screenshots/2-helloworld-health.jpg)

4. Comprobamos las métricas de los 2 endpoints en http://localhost:8000/ haciendo varias peticiones vía curl.
- Primeos podemos llamar al endpoint "/"
    ```sh
      curl -X 'GET' \
      'http://localhost:8081/' \
      -H 'accept: application/json'
    ```
- Luego al endpoint "/health"

    ```sh
      curl -X 'GET' \
      'http://localhost:8081/health' \
      -H 'accept: application/json'
    ```
    ![Métricas](Screenshots/3-logs.jpg)

5. Ejecutamos los tests de las 3 formas posibles (SIEMPRE DENTRO DEL ENTORNO VIRTUAL):
    ```sh
    pytest
    ```
    ```sh
    pytest --cov
    ```
    ```sh
    pytest --cov --cov-report=html
    ```
    ![Pytests](Screenshots/4-tests.jpg)



Una vez comprobado todo y a partir de ello, es necesario realizar una serie de mejoras:

### Mejorando el proyecto (Inicio de la práctica)

- Añadir por lo menos un nuevo endpoint a los existentes `/` y `/health`, un ejemplo sería `/bye` que devolvería `{"msg": "Bye Bye"}`, para ello será necesario añadirlo en el fichero [src/application/app.py](./src/application/app.py)
  - Hemos añadido el endpoint `/bye`, el cual da un mensaje en http://localhost:8081/bye `{"msg": "Bye, have a nice day"}`

- Creación de tests unitarios para el nuevo endpoint añadido, para ello será necesario modificar el [fichero de tests](./src/tests/app_test.py) 

  ![PytestsNewEndpoint](Screenshots/5-testsnew.jpg)


- Opcionalmente creación de helm chart para desplegar la aplicación en Kubernetes, se dispone de un ejemplo de ello en el laboratorio realizado en la clase 3

  - Acceso al helm chart --> [`LP-Chart`](LP-Chart/)

- Creación de pipelines de CI/CD en cualquier plataforma (Github Actions, Jenkins, etc) que cuenten por lo menos con las siguientes fases:

  - Testing: tests unitarios con cobertura. --> ['Testing pipeline'](.github\workflows/test.yaml)

    - Este flujo de trabajo automatiza la ejecución de pruebas, el análisis de cobertura y la generación de un informe detallado de cobertura cada vez que se realiza un push en la rama main

    ![Pipelinetesting1](Screenshots/6-pipelinetesting1.jpg)
    ![Pipelinetesting2](Screenshots/6-pipelinetesting2.jpg)
    
  - Build & Push: Creación de imagen docker y push de la misma a cualquier registry válido que utilice alguna estrategia de release para los tags de las vistas en clase, se recomienda GHCR ya incluido en los repositorios de Github. --> ['Build&Push pipeline'](.github\workflows/release.yaml)
    - Al hacer el commit, primero hay que guardar los cambios con un push normal.
    - Luego para taggear la version y que se ejecute el pipeline de release se deben usar los siguientes comandos: (Ejemplo si se quiere pasar a la versión 1.0.13).

    ```sh
    git tag v1.0.13
    ```
    - Seguido de:

    ```sh
    git push origin v1.0.13
    ```

      ![Pipelinerelease](Screenshots/7-pipelinerelease.jpg)

    - Este flujo de trabajo se encarga de construir una imagen Docker y publicarla en GHCR cada vez que se realiza un push con una etiqueta que comienza con 'v', tal como hemos mencionado anteriormente. Esto permite un proceso controlado de versionado y distribución de la imagen Docker asociada al proyecto.

    - Si todo funciona correctamente, en la sección Packages aparecerá el paquete Docker versionado y listo para su uso.
    - Podremos hacer un pull de ese docker y luego un run del mismo en nuestra terminal.

      ![Packages](Screenshots/8-packages.jpg)
      ![Packages2](Screenshots/8-packages2.jpg)

    - El script para comprobar que funcione el Docker que hemos creado en el Build&Push es el siguiente:

      ```sh
      docker run -p 8081:8081 -p 8000:8000 ghcr.io/albertferal/liberandoproductos:1.0.12
      ```

      - Es importante escribir bien el tag, en este caso la última versión publicada es la v1.0.12

- Configuración de monitorización y alertas:

  - Configurar monitorización mediante prometheus en los nuevos endpoints añadidos, por lo menos con la siguiente configuración:
    - Contador cada vez que se pasa por el/los nuevo/s endpoint/s, tal y como se ha realizado para los endpoints implementados inicialmente

      - Para ello modificamos el archivo [`app.py`](liberando-productos-practica-final/src/application/app.py) añadiendo métricas para el endpoint "/bye"
      - Comprobamos que funcionen llamando a dicho endpoint con curl:

      ```sh
        curl -X 'GET''http://localhost:8081/bye'-H 'accept: application/json'
      ```
      - En http://localhost:8000 deberíamos ver algo similar a esto:

      ![CounterBye](Screenshots/9-contadorbye.jpg)

  - Desplegar prometheus a través de Kubernetes mediante minikube y configurar alert-manager para por lo menos las siguientes alarmas, tal y como se ha realizado en el laboratorio del día 3 mediante el chart `kube-prometheus-stack`:
    - Uso de CPU de un contenedor mayor al del límite configurado, se puede utilizar como base el ejemplo utilizado en el laboratorio 3 para mandar alarmas cuando el contenedor de la aplicación `fast-api` consumía más del asignado mediante request

  - Las alarmas configuradas deberán tener severity high o critical

          - alert: CPUUsageExceeds75Percent
            expr: (sum(rate(container_cpu_usage_seconds_total{container!="",pod!=""}[5m]))
            / sum (kube_pod_container_resource_limits_cpu_cores) * 100) > 75
            for: 1m
            labels:
              severity: high
            annotations:
              summary: CPU Usage Exceeds 75%
              description: "CPU usage in containers exceeds 75%"


          - alert: CPUUsageExceedsLimit
            expr: avg(container_cpu_usage_seconds_total{job="kubernetes-nodes"}) by (pod)
            / avg(container_spec_cpu_quota{job="kubernetes-nodes"}) by (pod) * 100 > 100
            for: 1m
            labels:
              severity: critical
            annotations:
              summary: CPU Usage Exceeds Limit ({{ $labels.instance }})
              description: "CPU usage in container is above the configured limit"
        
    - Hemos añadido a [`values.yaml`](kube-prometheus-stack\values.yaml) de kube-prometheus-stack un par de reglas para que, cuando se cumplan, nos envíen notifiaciones en el canal de slack.
      - La 1a regla es de severity "high", su función (expr), es calcular la tasa de uso de CPU promedio durante los últimos 5 minutos y lo compara con el límite del 75% de la capacidad total de CPU asignada a los contenedores.
      - La 2a regla es de severity "critical", su función (expr), evalúa si el uso promedio de CPU en los contenedores supera el límite configurado del 100% de la capacidad asignada.


  - Crear canal en slack `<nombreAlumno>-prometheus-alarms` y configurar webhook entrante para envío de alertas con alert manager

  - Alert manager estará configurado para lo siguiente:
    - Mandar un mensaje a Slack en el canal configurado en el paso anterior con las alertas con label "severity" y "critical"
    - Deberán enviarse tanto alarmas como recuperación de las mismas
    - Habrá una plantilla configurada para el envío de alarmas

    Para poder comprobar si esta parte funciona se recomienda realizar una prueba de estres, como la realizada en el laboratorio 3 a partir del paso 8.

  - Creación de un dashboard de Grafana, con por lo menos lo siguiente:
    - Número de llamadas a los endpoints
    - Número de veces que la aplicación ha arrancado

## Entregables

Se deberá entregar mediante un repositorio realizado a partir del original lo siguiente:

- Código de la aplicación y los tests modificados
- Ficheros para CI/CD configurados y ejemplos de ejecución válidos
- Ficheros para despliegue y configuración de prometheus de todo lo relacionado con este, así como el dashboard creado exportado a `JSON` para poder reproducirlo
- `README.md` donde se explique como se ha abordado cada uno de los puntos requeridos en el apartado anterior, con ejemplos prácticos y guía para poder reproducir cada uno de ellos


URL WEBHOOK:
https://hooks.slack.com/services/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