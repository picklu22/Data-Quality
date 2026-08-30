import pytest

from Src.Snowflake_Connection import get_connection
from Src.excel_reader import read_rules


@pytest.fixture(scope="session")
def snowflake_connection():

    connection = get_connection()

    yield connection

    connection.close()


@pytest.fixture(scope="session")
def dq_rules():

    return read_rules(
        "test_data/data_quality_requirements.xlsx"
    )
