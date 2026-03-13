from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path

from .models import ExtractRequest
from .service import run_extraction


LEDGER_GROUP_OPTIONS = [
    "Primary",
    "Current Assets",
    "Current Liabilities",
    "Indirect Expenses",
    "Sales Accounts",
]

VOUCHER_TYPE_OPTIONS = [
    "All",
    "Payment",
    "Receipt",
    "Sales",
    "Purchase",
    "Journal",
    "Contra",
]

EXPORT_TYPE_OPTIONS = ["Ledger + Voucher", "Ledger Only", "Voucher Only"]


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Expected date in YYYY-MM-DD format") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract Tally ODBC data and save analysis-ready Excel output."
    )
    parser.add_argument("--company-name", required=True, help="Tally company name")
    parser.add_argument("--date-from", type=parse_date, required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--date-to", type=parse_date, required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument(
        "--ledger-group",
        default="Primary",
        choices=LEDGER_GROUP_OPTIONS,
        help="Ledger group filter",
    )
    parser.add_argument(
        "--voucher-type",
        default="All",
        choices=VOUCHER_TYPE_OPTIONS,
        help="Voucher type filter",
    )
    parser.add_argument(
        "--export-type",
        default="Ledger + Voucher",
        choices=EXPORT_TYPE_OPTIONS,
        help="Choose output scope",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tally_ledger_extract.xlsx"),
        help="Output Excel file path",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.date_from > args.date_to:
        parser.error("--date-from must be before or equal to --date-to")

    request = ExtractRequest(
        company_name=args.company_name.strip(),
        date_from=args.date_from,
        date_to=args.date_to,
        ledger_group=args.ledger_group,
        voucher_type=args.voucher_type,
        export_type=args.export_type,
    )

    result = run_extraction(request)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(result.workbook_bytes)

    print(f"Saved {len(result.raw_data)} rows to {args.output.resolve()}")


if __name__ == "__main__":
    main()
