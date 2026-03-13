from __future__ import annotations

from io import BytesIO

import pandas as pd


def build_excel_workbook(
    raw_data: pd.DataFrame,
    ledger_summary: pd.DataFrame,
    monthly_summary: pd.DataFrame,
    expense_heads: pd.DataFrame,
) -> bytes:
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        raw_data.to_excel(writer, sheet_name="Raw_Data", index=False)
        ledger_summary.to_excel(writer, sheet_name="Ledger_Summary", index=False)
        monthly_summary.to_excel(writer, sheet_name="Monthly_Summary", index=False)
        expense_heads.to_excel(writer, sheet_name="Expense_Heads", index=False)

    output.seek(0)
    return output.getvalue()
