import pandas as pd
import logging

# Configurando el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_data(engine):
    """
    Extrae datos de la base de datos y los guarda en un archivo Parquet.
    
    El formato Parquet es seleccionado debido a su eficiencia en espacio y tiempo de lectura, ideal para grandes volúmenes de datos.
    
    Retorna:
        tuple: Estado de la operación (bool) y el path del archivo generado o None.
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql('SELECT * FROM "data_nt"', connection)
            if df.empty:
                logging.warning("No se encontraron datos para extraer.")
                return False, None
            else:
                file_path = 'extracted_data.parquet'
                df.to_parquet(file_path)
                logging.info("Datos extraídos exitosamente a 'extracted_data.parquet'")
                return True, file_path
    except Exception as e:
        logging.error(f"Error al extraer los datos: {e}")
        return False, None


