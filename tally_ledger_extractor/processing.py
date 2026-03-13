from __future__ import annotations

import pandas as pd


def _ensure_datetime(frame: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_datetime(frame[column], errors="coerce")


def build_analysis_table(vouchers: pd.DataFrame, voucher_entries: pd.DataFrame) -> pd.DataFrame:
    if vouchers.empty or voucher_entries.empty:
        return pd.DataFrame(
            columns=[
                "Date",
                "Voucher Number",
                "Ledger Name",
                "Debit",
                "Credit",
                "Narration",
            ]
        )

    merged = voucher_entries.merge(
        vouchers[["VoucherDate", "VoucherNumber", "Narration"]],
        on=["VoucherDate", "VoucherNumber"],
        how="left",
    )

    merged["Amount"] = pd.to_numeric(merged["Amount"], errors="coerce").fillna(0)
    merged["Debit"] = merged["Amount"].where(merged["Amount"] > 0, 0)
    merged["Credit"] = (-merged["Amount"]).where(merged["Amount"] < 0, 0)

    output = pd.DataFrame(
        {
            "Date": _ensure_datetime(merged, "VoucherDate").dt.date,
            "Voucher Number": merged["VoucherNumber"],
            "Ledger Name": merged["LedgerName"],
            "Debit": merged["Debit"],
            "Credit": merged["Credit"],
            "Narration": merged["Narration"].fillna(""),
        }
    )

    return output.sort_values(["Date", "Voucher Number", "Ledger Name"]).reset_index(drop=True)


def build_ledger_summary(processed: pd.DataFrame) -> pd.DataFrame:
    if processed.empty:
        return pd.DataFrame(columns=["Ledger Name", "Debit", "Credit", "Balance"])

    summary = (
        processed.groupby("Ledger Name", dropna=False)[["Debit", "Credit"]]
        .sum()
        .reset_index()
    )
    summary["Balance"] = summary["Debit"] - summary["Credit"]
    return summary.sort_values("Ledger Name").reset_index(drop=True)


def build_monthly_summary(processed: pd.DataFrame) -> pd.DataFrame:
    if processed.empty:
        return pd.DataFrame(columns=["Month", "Debit", "Credit", "Balance"])

    data = processed.copy()
    data["Month"] = pd.to_datetime(data["Date"], errors="coerce").dt.to_period("M").astype(str)
    summary = data.groupby("Month")[["Debit", "Credit"]].sum().reset_index()
    summary["Balance"] = summary["Debit"] - summary["Credit"]
    return summary.sort_values("Month").reset_index(drop=True)


def build_expense_heads(processed: pd.DataFrame) -> pd.DataFrame:
    if processed.empty:
        return pd.DataFrame(columns=["Ledger Name", "Total Expense"])

    expense_rows = processed[processed["Debit"] > 0]
    summary = (
        expense_rows.groupby("Ledger Name", dropna=False)["Debit"]
        .sum()
        .reset_index(name="Total Expense")
        .sort_values("Total Expense", ascending=False)
    )
    return summary.reset_index(drop=True)
