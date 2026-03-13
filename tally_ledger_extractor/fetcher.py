from __future__ import annotations

from typing import Any

import pandas as pd

from .models import ExtractRequest


def _safe_read_sql(query: str, connection: Any) -> pd.DataFrame:
    try:
        return pd.read_sql(query, connection)
    except Exception:
        return pd.DataFrame()


def _quote(value: str) -> str:
    return value.replace("'", "''")


def fetch_ledgers(connection: Any, request: ExtractRequest) -> pd.DataFrame:
    group_filter = ""
    if request.ledger_group != "All":
        group_filter = f"WHERE $Parent = '{_quote(request.ledger_group)}'"

    query = (
        "SELECT $Name AS LedgerName, $Parent AS LedgerGroup "
        "FROM Ledger "
        f"{group_filter}"
    )
    return _safe_read_sql(query, connection)


def fetch_vouchers(connection: Any, request: ExtractRequest) -> pd.DataFrame:
    filters = [
        f"$Date >= '{request.date_from_sql}'",
        f"$Date <= '{request.date_to_sql}'",
    ]
    if request.voucher_type != "All":
        filters.append(f"$VoucherTypeName = '{_quote(request.voucher_type)}'")

    where_clause = " AND ".join(filters)
    query = (
        "SELECT $Date AS VoucherDate, $VoucherNumber AS VoucherNumber, "
        "$VoucherTypeName AS VoucherType, $Narration AS Narration "
        "FROM Voucher "
        f"WHERE {where_clause}"
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


def _apply_company_filter(frame: pd.DataFrame, request: ExtractRequest) -> pd.DataFrame:
    if frame.empty:
        return frame

    company_columns = [
        col for col in frame.columns if col.lower() in {"company", "companyname", "company_name"}
    ]
    if not company_columns:
        return frame

    company_col = company_columns[0]
    return frame[
        frame[company_col].astype(str).str.strip().str.casefold() == request.company_name.strip().casefold()
    ]


def fetch_all(connection: Any, request: ExtractRequest) -> dict[str, pd.DataFrame]:
    ledgers = fetch_ledgers(connection, request)
    vouchers = fetch_vouchers(connection, request)
    voucher_entries = fetch_voucher_entries(connection, request)

    return {
        "ledgers": _apply_company_filter(ledgers, request),
        "vouchers": _apply_company_filter(vouchers, request),
        "voucher_entries": _apply_company_filter(voucher_entries, request),
        "groups": fetch_groups(connection),
    }
