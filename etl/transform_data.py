import pandas as pd
import logging
from sqlalchemy import types

# Configurando el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_data(file_path):
    """
    Transforma datos extraídos y los almacena en nuevas tablas.
    Argumento:
    file_path: La ubicación del archivo Parquet de donde se leerán los datos.
    """
    try:
        df = read_data(file_path)
        companies_df, charges_df = process_transformations(df)
        return companies_df, charges_df
    except Exception as e:
        logging.error(f"Error en la transformación de datos: {e}")

def read_data(file_path):
    """Lee los datos desde un archivo parquet."""
    try:
        df = pd.read_parquet(file_path)
        logging.info("Datos leídos desde archivo Parquet.")
        return df
    except Exception as e:
        logging.error(f"No se pudo leer el archivo Parquet: {e}")
        return None

def process_transformations(df):
    """Aplica transformaciones al DataFrame según el esquema propuesto."""
    df.rename(columns={'name': 'company_name', 'paid_at': 'updated_at'}, inplace=True)
    df['company_name'] = df['company_name'].astype(str).fillna('Unknown')  # Asumiendo que puede haber nulos
    df['updated_at'] = pd.to_datetime(df['updated_at']).fillna(pd.Timestamp.now())   # Rellenar valores nulos en 'updated_at' y convertir a timestamp
    df = df.astype({
        'id': str,
        'company_id': str,
        'amount': float,
        'status': str,
        'created_at': 'datetime64[ns]',
        'updated_at': 'datetime64[ns]'
    })

    # Aplicar validación de amount antes de continuar
    df = validate_amount(df)

    # Crear DataFrame para 'companies'
    companies_df = df[['company_id', 'company_name']].drop_duplicates().reset_index(drop=True)

    # Crear DataFrame para 'charges'
    charges_df = df[['id', 'company_id', 'amount', 'status', 'created_at', 'updated_at']]

    logging.info("Transformaciones aplicadas a los datos.")
    return companies_df, charges_df

def validate_amount(df):

    # DETAIL: A field with precision 16, scale 2 must round to an absolute value less than 10^14.
    max_value = 99999999999999.99
    if (df['amount'] > max_value).any():
        logging.warning("Se detectaron valores excesivos en 'amount', que serán ajustados al máximo permitido.")
    df['amount'] = df['amount'].apply(lambda x: min(x, max_value) if pd.notnull(x) else x)
    return df


def truncate_ids(df, column_name, max_length=24):
    """
    Truncates the values in the specified column of the DataFrame to the specified max_length.
    """
    df[column_name] = df[column_name].apply(lambda x: x[:max_length] if isinstance(x, str) else x)
    return df

def save_transformed_data(engine, companies_df, charges_df):
    """Guarda los DataFrames transformados en la base de datos."""
    
    # Truncar los IDs en companies_df y charges_df antes de cargarlos
    companies_df = truncate_ids(companies_df, 'company_id', 24)
    charges_df = truncate_ids(charges_df, 'company_id', 24)
    charges_df = truncate_ids(charges_df, 'id', 24)

    with engine.begin() as connection:
        companies_df.to_sql('companies', connection, if_exists='replace', index=False, dtype={
            'company_id': types.VARCHAR(24),
            'company_name': types.VARCHAR(130)
        })
        charges_df.to_sql('charges', connection, if_exists='replace', index=False, dtype={
            'id': types.VARCHAR(24),
            'company_id': types.VARCHAR(24),
            'amount': types.DECIMAL(precision=16, scale=2),
            'status': types.VARCHAR(30),
            'created_at': types.TIMESTAMP,
            'updated_at': types.TIMESTAMP
        })
        try:
            connection.execute("""
                ALTER TABLE charges
                ADD CONSTRAINT fk_company
                FOREIGN KEY (company_id)
                REFERENCES companies (company_id)
            """)
        except Exception as e:
            logging.info(f"La clave foránea ya existe o hubo un error al crearla: {e}")
        logging.info("Datos guardados en las tablas 'companies' y 'charges'.")


