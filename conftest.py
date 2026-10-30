from collections.abc import Generator
from typing import Any

import pymysql
import pytest
from pymysql.connections import Connection
from pymysql.cursors import Cursor, DictCursor


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--host", action="store", default="localhost", help="Host address")
    parser.addoption("--port", action="store", default=3306, help="Port number")
    parser.addoption("--database", action="store", default="prestashop", help="Database name")
    parser.addoption("--user", action="store", default="root", help="User name")
    parser.addoption("--password", action="store", default="admin", help="Password")

@pytest.fixture(scope="session")
def connection(request: pytest.FixtureRequest) -> Generator[Connection[Cursor], Any, None]:
    connection = pymysql.connect(host=request.config.getoption("--host"),
                                         port=request.config.getoption("--port"),
                                         database=request.config.getoption("--database"),
                                         user=request.config.getoption("--user"),
                                         password=request.config.getoption("--password"),
                                         cursorclass=DictCursor)
    yield connection
    connection.close()

@pytest.fixture(scope="function")
def cursor(connection: Connection) -> Generator[Cursor, None, None]:
    cursor = connection.cursor()
    yield cursor
    cursor.close()
    connection.rollback()