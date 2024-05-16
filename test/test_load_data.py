import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from etl.load_data import load_data

@pytest.fixture
def engine_mock():
    # Mock del motor SQLAlchemy
    return MagicMock()

@patch("etl.load_data.pd.read_csv")
def test_load_data_success(mock_read_csv, engine_mock):
    # Mock del DataFrame de pandas
    df_mock = MagicMock()
    mock_read_csv.return_value = df_mock

    # Llamada a la función con el mock
    result = load_data(engine_mock, "fake_file.csv")

    # Verificaciones
    assert result == True
    mock_read_csv.assert_called_once_with("fake_file.csv")
    df_mock.to_sql.assert_called_once_with('table_name', con=engine_mock, if_exists='append', index=False)

@patch("etl.load_data.pd.read_csv")
def test_load_data_failure(mock_read_csv, engine_mock):
    # Simulación de excepción en read_csv
    mock_read_csv.side_effect = Exception("Error de lectura")

    # Llamada a la función con el mock
    result = load_data(engine_mock, "fake_file.csv")

    # Verificaciones
    assert result == False
    mock_read_csv.assert_called_once_with("fake_file.csv")
    engine_mock.connect.assert_not_called()
