# Prueba Técnica NT

Este proyecto incluye una API desarrollada con FastAPI y un proceso ETL, ambos configurados para ejecutarse en contenedores Docker.

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

    Crea el archivo .env en la raíz del proyecto y modifica las variables de entorno:
  
    Ejemplo de variables de entorno 
    ```
    POSTGRES_USER=user
    POSTGRES_PASSWORD=8Q8sElMuJSBfPRg
    POSTGRES_DB=mydatabase
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
    ```


## Despliegue con Docker Compose

El proyecto puede ejecutarse en dos modos distintos: `etl` para ejecutar el proceso de ETL  y `api` para ejecutar una API. El modo de operación se controla mediante la variable de entorno `APP_MODE` en el archivo `docker-compose.yml`.

### Configuración del `docker-compose.yml`

El archivo `docker-compose.yml` está configurado para utilizar una base de datos PostgreSQL y un contenedor de aplicación que puede ejecutar tanto el proceso de ETL como la API, dependiendo del valor de `APP_MODE`.

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - APP_MODE=etl # Cambia a 'etl' para ejecutar el proceso ETL o 'api' para ejecutar la API
    env_file:
      - .env

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```
### Cambiar el Modo de Operación
  Para cambiar entre el proceso de ETL y la API, simplemente modifica el valor de APP_MODE en el archivo docker-compose.yml.

#### Para ejecutar el proceso de ETL:

  ```yaml
    environment:
      - APP_MODE=etl
  ```
####  Para ejecutar la API:

  ```yaml
    environment:
      - APP_MODE=api
  ```
### Ejecutar Docker Compose
  Después de configurar APP_MODE en el modo deseado, ejecuta Docker Compose con el siguiente comando:

  ```sh
  docker-compose up --build
  ```
### Acceso a la API

  La API estará disponible en http://localhost:8000. Puedes interactuar con ella usando herramientas como cURL, Postman o simplemente a través de tu navegador para acceder a la documentación automática generada por FastAPI en http://localhost:8000/docs.
   
Este comando construirá y levantará los servicios definidos en el archivo docker-compose.yml.
## Limpieza
  Para detener y remover todos los contenedores, redes y volúmenes creados por Docker Compose, ejecuta:

  ```bash
  docker-compose down -v
  ```


## Cómo ejecutar los tests
 Sigue estos pasos para ejecutar los tests del proyecto:

### Configurar el PYTHONPATH (opcional pero recomendado)

En Linux/Mac:

```sh
export PYTHONPATH=$(pwd)
```
En Windows:

```sh
set PYTHONPATH=%cd%
```

 ### Crear un entorno virtual

```sh
python -m venv venv
```

### Activar el entorno virtual

En Linux/Mac:

```sh
source venv/bin/activate
```

En Windows:

```sh
.\venv\Scripts\activate
```

### Instalar las dependencias necesarias

```sh
pip install pytest pandas sqlalchemy
```
### Ejecutar pytest para correr los tests

```sh
pytest
```

Con estos pasos, deberías poder ejecutar los tests y verificar las funciones del proyecto funcionan correctamente.

