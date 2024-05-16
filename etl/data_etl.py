from sqlalchemy import create_engine
import logging
import os
from load_data import load_data
from extract_data import extract_data
from transform_data import transform_data, save_transformed_data
from dotenv import load_dotenv
from create_view import check_and_create_view , create_view

# Configuración avanzada de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[logging.FileHandler("etl.log"), logging.StreamHandler()])

def main():
    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)

    try:
        # Paso 1: Cargar datos en la base de datos desde un CSV
        logging.info("Iniciando la carga de datos.")
        if not load_data(engine):
            logging.error("La carga de datos falló.")
            return
        logging.info("Carga de datos completada exitosamente.")

        # Paso 2: Extraer datos de la base de datos y guardarlos en un archivo Parquet
        logging.info("Iniciando la extracción de datos.")
        extract_success, file_path = extract_data(engine)
        if not extract_success:
            logging.error("La extracción de datos falló.")
            return
        logging.info("Extracción de datos completada exitosamente.")

        # Paso 3: Transformar los datos y prepararlos para la carga
        logging.info("Iniciando la transformación de datos.")
        companies_df, charges_df = transform_data(file_path)
        if companies_df is None or charges_df is None:
            logging.error("La transformación de datos falló.")
            return
        logging.info("Transformación de datos completada exitosamente.")

        # Paso 4: Cargar los datos transformados en las tablas 'companies' y 'charges'
        logging.info("Iniciando la carga de datos transformados.")
        save_transformed_data(engine, companies_df, charges_df)
        logging.info("Datos transformados cargados exitosamente en la base de datos.")

        # Paso 5: Crear la vista después de cargar los datos
        logging.info("Iniciando la creación de la vista.")
        create_view(engine)
        logging.info("Creación de la vista con éxito.")

        # Paso final: Verifica y crea la vista si es necesario
        check_and_create_view(engine)
        logging.info("Proceso ETL completado con éxito.")

    except Exception as e:
        logging.error(f"Error en el proceso ETL: {e}")

if __name__ == "__main__":
    main()




