## Desplegando prometheus a través de Minikube

1. Crear un cluster de Kubernetes que utilice la versión `v1.21.1` utilizando minikube para ello a través de un nuevo perfil llamado `monitoring-project`:

    ```sh
    minikube start --kubernetes-version='v1.28.3' \
        --cpus=4 \
        --memory=4096 \
        --addons="metrics-server,default-storageclass,storage-provisioner" \
        -p monitoring-project
    ```

2. Modificar el fichero [kube-prometheus-stack/values.yaml](kube-prometheus-stack/values.yaml) añadiendo el canal al que se enviarán las alarmas, así como la URL del webhook configurado previamente en Slack.

3. Añadir el repositorio de helm `prometheus-community` para poder desplegar el chart `kube-prometheus-stack`:

    ```sh
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    ```

4. Desplegar el chart `kube-prometheus-stack` del repositorio de helm añadido en el paso anterior con los valores configurados en el archivo [kube-prometheus-stack/values.yaml](kube-prometheus-stack/values.yaml) en el namespace `monitoring`:

    ```sh
    helm -n monitoring upgrade \
        --install prometheus \
        prometheus-community/kube-prometheus-stack \
        -f kube-prometheus-stack/values.yaml \
        --create-namespace \
        --wait --version 55.4.0
    ```

5. Realizar split de la terminal o crear una nueva pestaña y ver como se están creando pod en el namespace `monitoring` utilizado para desplegar el stack de prometheus:

    ```sh
    kubectl -n monitoring get po -w
    ```

6. Añadir el repositorio de helm de mongodb para poder desplegar el operador de base de datos de mongodb:

    ```sh
    helm repo add mongodb https://mongodb.github.io/helm-charts
    ```

7. Actualizar los repositorios de helm:

    ```sh
    helm repo update
    ```

8. Desplegar el helm chart del operador de mongodb:

    ```sh
    helm upgrade --install community-operator \
        mongodb/community-operator \
        -n mongodb --create-namespace \
        --wait --version 0.9.0
    ```

Se ha creado un helm chart en la carpeta `fast-api-webapp` para la aplicación de la práctica, en la cual se  dispone de métricas mediante prometheus. Para desplegarlo es necesario realizar los siguientes pasos:

 1. Desplegar el helm chart:

    ```sh
    helm -n fast-api upgrade my-app --wait --install --create-namespace fast-api-webapp
    ```

2. Hacer split de la terminal o crear una nueva pestaña en la misma y observar como se crean los pods en el namespace `fast-api` donde se ha desplegado el web server:

    ```sh
    kubectl -n fast-api get po -w
    ```

3. Hacer nuevamente split de la terminal o abrir una nueva pestaña en la misma y comprobar como se está creando un recurso de tipo `mongodb` para disponer de un cluster de Mongo:

    ```sh
    kubectl get -n mongodb mongodbcommunity -w
    ```

    La salida de este comando debería ser algo como lo siguiente:

    ```sh
    NAME      PHASE     VERSION
    mongodb   Pending
    ```

    Esperar hasta que el valor de `PHASE` pase a `Running`, esto indicará que se dispone de un cluster de MongoDB

    ```sh
    NAME      PHASE     VERSION
    mongodb   Running   5.0.6
    ```

4. Se puede comprobar a través de los endpoints disponibles del servicio creado:

    ```sh
    kubectl -n mongodb get ep mongodb-svc
    ```

    El resultado del comando anterior debería ser algo como lo siguiente:

    ```sh
    NAME          ENDPOINTS                                                        AGE
    mongodb-svc   10.244.0.13:9216,10.244.0.14:9216,10.244.0.15:9216 + 3 more...   4m1s
    ```

5. Hacer de nuevo split de la terminal o crear una nueva pestaña y obtener los logs del container `wait-mongo` del deployment `my-app-fast-api-webapp` en el namespace `fast-api`, observar como está utilizando ese contenedor para esperar a que MongoDB esté listo:

    ```sh
    kubectl -n fast-api logs -f deployment/my-app-fast-api-webapp -c wait-mongo
    ```

    Una vez se obtenga el mensaje de conexión exitosa a mongo, siendo algo como lo mostrado a continuación, indicará que empezará el contenedor `fast-api-webapp`:

    ```sh
    mongodb-svc.mongodb.svc.cluster.local (10.244.0.13:27017) open
    ```

6. Obtener los logs del contenedor `fast-api-webapp` del deployment `my-app-fast-api-webapp` en el namespace `fast-api`, observar como está arrancando el servidor fast-api:

    ```sh
    kubectl -n fast-api logs -f deployment/my-app-fast-api-webapp -c fast-api-webapp
    ```

    Debería obtenerse un resultado similar al siguiente:

    ```sh
    [2022-11-09 11:28:12 +0000] [1] [INFO] Running on http://0.0.0.0:8081 (CTRL + C to quit)
    ```

## Port-forwarding para ver todo lo desplegado hasta el momento:

- Abrir una nueva pestaña en la terminal y realizar un port-forward del puerto `http-web` del servicio de Grafana al puerto 3000 de la máquina. 

    ```sh
    kubectl -n monitoring port-forward svc/prometheus-grafana 3000:http-web
    ```
    - Acceder a la dirección `http://localhost:3000` en el navegador para acceder a Grafana, las credenciales por defecto son `admin` para el usuario y `prom-operator` para la contraseña.

- Abrir otra pestaña en la terminal y realizar un port-forward del servicio de Prometheus al puerto 9090 de la máquina:

    ```sh
    kubectl -n monitoring port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
    ```

- Abrir dos nuevas pestañas en la terminal y realizar dos port-forwards al `Service` creado para nuestro servidor (8081 para la web y 8000 para las métricas):

    ```sh
    kubectl -n fast-api port-forward svc/my-app-fast-api-webapp 8081:8081
    ```
     ```sh
    kubectl -n fast-api port-forward svc/my-app-fast-api-webapp 8000:8000
    ```
