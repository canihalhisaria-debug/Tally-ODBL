from __future__ import annotations

from typing import Any

import pandas as pd

from .models import ExtractRequest


def _safe_read_sql(query: str, connection: Any) -> pd.DataFrame:
    try:
        return pd.read_sql(query, connection)
    except Exception:
        return pd.DataFrame()


def fetch_ledgers(connection: Any, request: ExtractRequest) -> pd.DataFrame:
    query = (
        "SELECT $Name AS LedgerName, $Parent AS LedgerGroup "
        "FROM Ledger "
        f"WHERE $Parent = '{_quote(request.ledger_group)}'"
    )
    return _safe_read_sql(query, connection)


def _quote(value: str) -> str:
    return value.replace("'", "''")


def fetch_vouchers(connection: Any, request: ExtractRequest) -> pd.DataFrame:
    voucher_filter = ""
    if request.voucher_type != "All":
        voucher_filter = f"AND $VoucherTypeName = '{_quote(request.voucher_type)}' "

    query = (
        "SELECT $Date AS VoucherDate, $VoucherNumber AS VoucherNumber, "
        "$VoucherTypeName AS VoucherType, $Narration AS Narration "
        "FROM Voucher "
        f"WHERE $Date >= '{request.date_from_sql}' "
        f"AND $Date <= '{request.date_to_sql}' "
        f"{voucher_filter}"
    )
    return _safe_read_sql(query, connection)


def fetch_voucher_entries(connection: Any, request: ExtractRequest) -> pd.DataFrame:
    query = (
        "SELECT $Date AS VoucherDate, $VoucherNumber AS VoucherNumber, "
        "$LedgerName AS LedgerName, $Amount AS Amount "
        "FROM LedgerEntries "
        f"WHERE $Date >= '{request.date_from_sql}' "
        f"AND $Date <= '{request.date_to_sql}'"
    )
    return _safe_read_sql(query, connection)


def fetch_groups(connection: Any) -> pd.DataFrame:
    query = "SELECT $Name AS GroupName FROM Group"
    return _safe_read_sql(query, connection)


def fetch_all(connection: Any, request: ExtractRequest) -> dict[str, pd.DataFrame]:
    return {
        "ledgers": fetch_ledgers(connection, request),
        "vouchers": fetch_vouchers(connection, request),
        "voucher_entries": fetch_voucher_entries(connection, request),
        "groups": fetch_groups(connection),
    }
