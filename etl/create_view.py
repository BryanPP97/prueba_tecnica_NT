from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
import logging

def check_and_create_view(engine):
    check_view_sql = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.views
            WHERE table_schema = 'public'
            AND table_name = 'daily_company_transactions'
        );
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(check_view_sql).scalar()
            if result:
                logging.info("La vista 'daily_company_transactions' ya existe.")
            else:
                logging.warning("La vista 'daily_company_transactions' no existe, intentando crearla.")
                create_view(engine)
    except SQLAlchemyError as e:
        logging.error(f"Error de SQLAlchemy: {e}")
        create_view(engine)
    except Exception as e:
        logging.error(f"Error inesperado: {e}")

def create_view(engine):
    create_view_sql = text("""
        CREATE OR REPLACE VIEW public.daily_company_transactions AS
        SELECT
            c.company_name,
            DATE(ch.created_at) AS transaction_date,
            SUM(ch.amount) AS total_amount
        FROM
            charges ch
        JOIN
            companies c ON ch.company_id = c.company_id
        GROUP BY
            c.company_name, DATE(ch.created_at);
    """)
    
    try:
        with engine.connect() as conn:
            conn.execute(create_view_sql)
            conn.commit()
            logging.info("Vista 'daily_company_transactions' creada exitosamente.")
            # Verificación inmediata de la creación de la vista
            test_query_sql = text("SELECT 1 FROM daily_company_transactions LIMIT 1")
            test_query = conn.execute(test_query_sql).fetchone()
            if test_query:
                logging.info("Confirmación de la creación de la vista completada con éxito.")
            else:
                logging.error("No se pudo crear la vista correctamente.")
    except Exception as e:
        logging.error(f"No se pudo crear la vista: {e}")

