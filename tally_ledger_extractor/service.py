from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .connection import get_tally_connection
from .excel_export import build_excel_workbook
from .fetcher import fetch_all
from .models import ExtractRequest
from .processing import (
    build_analysis_table,
    build_expense_heads,
    build_ledger_summary,
    build_monthly_summary,
)


@dataclass
class ExtractResult:
    raw_data: pd.DataFrame
    ledger_summary: pd.DataFrame
    monthly_summary: pd.DataFrame
    expense_heads: pd.DataFrame
    workbook_bytes: bytes


def run_extraction(request: ExtractRequest) -> ExtractResult:
    with get_tally_connection() as connection:
        dataset = fetch_all(connection, request)

    raw_data = build_analysis_table(
        dataset["vouchers"],
        dataset["voucher_entries"],
    )
    ledger_summary = build_ledger_summary(raw_data)
    monthly_summary = build_monthly_summary(raw_data)
    expense_heads = build_expense_heads(raw_data)

    workbook = build_excel_workbook(
        raw_data=raw_data,
        ledger_summary=ledger_summary,
        monthly_summary=monthly_summary,
        expense_heads=expense_heads,
        export_type=request.export_type,
    )

    return ExtractResult(
        raw_data=raw_data,
        ledger_summary=ledger_summary,
        monthly_summary=monthly_summary,
        expense_heads=expense_heads,
        workbook_bytes=workbook,
    )
