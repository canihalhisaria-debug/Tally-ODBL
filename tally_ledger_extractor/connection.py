from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import pyodbc

DSN_NAME = "TallyODBC64_9000"


@contextmanager
def get_tally_connection() -> Iterator[pyodbc.Connection]:
    try:
        connection = pyodbc.connect(f"DSN={DSN_NAME}", autocommit=False)
    except pyodbc.Error as exc:
        raise ConnectionError(
            f"Unable to connect to Tally ODBC DSN '{DSN_NAME}'. "
            "Ensure TallyPrime is running, ODBC is enabled, and the DSN exists."
        ) from exc
    try:
        yield connection
    finally:
        connection.close()
