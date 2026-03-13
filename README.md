# Tally Ledger Extractor

Desktop-style Streamlit application for extracting ledger and voucher data from **TallyPrime** through ODBC DSN `TallyODBC64_9000` and exporting analysis-ready Excel workbooks.

## Stack
- Python backend
- Streamlit frontend
- pandas + openpyxl Excel export

## Modules Implemented
1. **Input Module**
   - Company Name
   - Date From / Date To
   - Ledger Group (including `All`)
   - Voucher Type
   - Export Type
2. **Connection Module**
   - ODBC connection via DSN `TallyODBC64_9000`
3. **Data Fetch Module**
   - Ledgers
   - Vouchers
   - Voucher entries
   - Groups
4. **Data Processing**
   - Processed table columns: Date, Voucher Number, Ledger Name, Debit, Credit, Narration
5. **Excel Output**
   - `Raw_Data`
   - `Ledger_Summary`
   - `Monthly_Summary`
   - `Expense_Heads`
6. **UI**
   - Streamlit controls with dropdowns/date inputs
   - Extract button and download button
7. **Output**
   - One-click Excel export for accounting analysis

## Run as command-line tool (Python)
```bash
python -m tally_ledger_extractor.cli \
  --company-name "My Company Pvt Ltd" \
  --date-from 2025-01-01 \
  --date-to 2025-03-31 \
  --ledger-group "Primary" \
  --voucher-type "All" \
  --export-type "Ledger + Voucher" \
  --output reports/tally_extract.xlsx
```

This generates an Excel file directly without opening the Streamlit UI.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

> Ensure TallyPrime ODBC server is running and DSN `TallyODBC64_9000` exists on the machine.

## Recent reliability fixes
- Better ODBC connection error when DSN/Tally service is unavailable.
- Support for `All` ledger groups in UI and CLI.
- Improved empty-result handling in Streamlit app with clear guidance instead of raw traceback.
- Company-name filtering is applied when returned tables include a company column.
