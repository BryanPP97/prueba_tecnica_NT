import pandas as pd
import logging

# Configurando el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(engine):
    """
    Carga la información desde un archivo CSV a una base de datos PostgreSQL.
    
    Argumentos:
    engine -- objeto de conexión SQLAlchemy Engine para interactuar con la base de datos
    
    Retorna:
        bool: True si la carga fue exitosa, False en caso contrario.
    """
    try:
        logging.info("Leyendo el archivo CSV.")
        df = pd.read_csv('data_NT.csv')
        logging.info("Archivo CSV leído correctamente. Iniciando la carga a la base de datos.")
        df.to_sql('data_nt', engine, if_exists='replace', index=False)
        logging.info("Datos cargados exitosamente en la base de datos.")
        return True
    except Exception as e:
        logging.error(f"Error al cargar los datos: {e}")
        return False
