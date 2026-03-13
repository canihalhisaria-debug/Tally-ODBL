from dataclasses import dataclass
from datetime import date


@dataclass
class ExtractRequest:
    company_name: str
    date_from: date
    date_to: date
    ledger_group: str
    voucher_type: str
    export_type: str

    @property
    def date_from_sql(self) -> str:
        return self.date_from.strftime("%Y%m%d")

    @property
    def date_to_sql(self) -> str:
        return self.date_to.strftime("%Y%m%d")
