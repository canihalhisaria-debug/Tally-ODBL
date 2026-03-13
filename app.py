from __future__ import annotations

from datetime import date

import streamlit as st

from tally_ledger_extractor.models import ExtractRequest
from tally_ledger_extractor.service import run_extraction

st.set_page_config(page_title="Tally Ledger Extractor", page_icon="📊", layout="wide")
st.title("Tally Ledger Extractor")
st.caption("Extract ledger and voucher data from TallyPrime via ODBC and export to Excel.")

with st.sidebar:
    st.header("Input Module")
    company_name = st.text_input("Company Name", value="")
    date_from = st.date_input("Date From", value=date(date.today().year, 1, 1))
    date_to = st.date_input("Date To", value=date.today())

    ledger_group = st.selectbox(
        "Ledger Group",
        ["All", "Primary", "Current Assets", "Current Liabilities", "Indirect Expenses", "Sales Accounts"],
    )
    voucher_type = st.selectbox(
        "Voucher Type",
        ["All", "Payment", "Receipt", "Sales", "Purchase", "Journal", "Contra"],
    )
    export_type = st.selectbox("Export Type", ["Ledger + Voucher", "Ledger Only", "Voucher Only"])

extract_clicked = st.button("Extract Data", type="primary")

if extract_clicked:
    if not company_name.strip():
        st.error("Company Name is required.")
    elif date_from > date_to:
        st.error("Date From must be before Date To.")
    else:
        request = ExtractRequest(
            company_name=company_name.strip(),
            date_from=date_from,
            date_to=date_to,
            ledger_group=ledger_group,
            voucher_type=voucher_type,
            export_type=export_type,
        )

        with st.spinner("Connecting to Tally ODBC and fetching data..."):
            try:
                result = run_extraction(request)
            except Exception as exc:
                st.error(str(exc))
            else:
                if result.raw_data.empty:
                    st.warning("No vouchers found for the selected filters. Try widening date range or voucher filters.")
                else:
                    st.success("Extraction complete.")
                st.subheader("Processed Data Preview")
                st.dataframe(result.raw_data, use_container_width=True)

                st.download_button(
                    "Download Excel",
                    data=result.workbook_bytes,
                    file_name="tally_ledger_extract.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

                c1, c2, c3 = st.columns(3)
                c1.metric("Rows", len(result.raw_data))
                c2.metric("Ledgers", len(result.ledger_summary))
                c3.metric("Months", len(result.monthly_summary))
