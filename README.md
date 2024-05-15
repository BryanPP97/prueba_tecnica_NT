# NPrueba Técnica Next Solutions

Breve descripción del proyecto: Este proyecto incluye una API desarrollada con FastAPI y un proceso ETL, ambos configurados para ejecutarse en contenedores Docker.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado Docker y Docker Compose en tu sistema. Visita [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/) para las guías de instalación.

## Configuración Inicial

1. **Clonar el Repositorio**

   Para obtener el proyecto, clona el repositorio en tu máquina local usando:

   ```bash
   git clone https://github.com/BryanPP97/prueba_tecnica_NT.git
   cd prueba_tecnica_NT

   ```
2. **Configuración de Variables de Entorno**

Copia el archivo de ejemplo .env.example a .env y modifica las variables de entorno:

Ejemplo de variables de entorno 

POSTGRES_USER=bryan
POSTGRES_PASSWORD=8Q8sElMuJSBfPRg
POSTGRES_DB=mydatabase
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}



## Despliegue con Docker Compose
Para poner en marcha el proyecto, sigue estos pasos:

1. Construir y Levantar los Servicios

    Desde la raíz del directorio del proyecto, ejecuta:

        ```bash
        docker-compose up --build
        ```
2. Verificación

    Asegúrate de que todos los contenedores están corriendo correctamente:

        ```bash
        docker-compose ps

        ```

3. Acceso a la API

    La API estará disponible en http://localhost:8000. Puedes interactuar con ella usando herramientas como cURL, Postman o simplemente a través de tu navegador para acceder a la documentación automática generada por FastAPI.

4.Ejecutar Comandos Adicionales

    Si necesitas ejecutar comandos adicionales en uno de tus contenedores, puedes hacerlo con:

    ```bash
    docker-compose exec NOMBRE_DEL_SERVICIO COMANDO
    ```

    Por ejemplo, para interactuar con la base de datos, puedes usar:

    ```bash
    docker compose exec db psql -U bryan -d mydatabase
    ```

## Limpieza
    Para detener y remover todos los contenedores, redes y volúmenes creados por Docker Compose, ejecuta:

    ```bash
    docker-compose down -v
    ```