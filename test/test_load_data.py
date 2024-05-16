import pytest
import pandas as pd
from sqlalchemy import create_engine
from unittest.mock import patch, MagicMock
from etl.load_data import load_data

# Crear un motor SQLite en memoria para las pruebas
@pytest.fixture(scope="module")
def engine():
    return create_engine('sqlite:///:memory:')

# Prueba para verificar si los datos se cargan correctamente
@patch("etl.load_data.pd.read_csv")
@patch("etl.load_data.pd.DataFrame.to_sql")
def test_load_data_success(mock_to_sql, mock_read_csv, engine):
    # Mock del DataFrame de pandas
    df_mock = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_read_csv.return_value = df_mock

    # Llamada a la función con el mock
    result = load_data(engine)

    # Verificar que la función retorna True
    assert result == True

    # Verificar que read_csv fue llamado con el archivo correcto
    mock_read_csv.assert_called_once_with('data_NT.csv')

    # Verificar que to_sql fue llamado correctamente
    mock_to_sql.assert_called_once_with('data_nt', engine, if_exists='replace', index=False)

# Prueba para verificar el manejo de excepciones
@patch("etl.load_data.pd.read_csv")
def test_load_data_failure(mock_read_csv, engine):
    # Simulación de excepción en read_csv
    mock_read_csv.side_effect = Exception("Error de lectura")

    # Llamada a la función con el mock
    result = load_data(engine)

    # Verificar que la función retorna False
    assert result == False

    # Verificar que read_csv fue llamado con el archivo correcto
    mock_read_csv.assert_called_once_with('data_NT.csv')
