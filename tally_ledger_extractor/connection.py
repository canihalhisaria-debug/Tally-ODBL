from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import pyodbc

DSN_NAME = "TallyODBC64_9000"


@contextmanager
def get_tally_connection() -> Iterator[pyodbc.Connection]:
    connection = pyodbc.connect(f"DSN={DSN_NAME}", autocommit=False)
    try:
        yield connection
    finally:
        connection.close()
