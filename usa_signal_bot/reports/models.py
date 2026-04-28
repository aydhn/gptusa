from dataclasses import dataclass
from typing import Optional
from ..core.domain import BaseDomainModel
from ..core.enums import ReportFormat

@dataclass
class ReportRequest(BaseDomainModel):
    report_name: str = ""
    report_format: ReportFormat = ReportFormat.TXT
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    include_sections: list[str] = None

    def __post_init__(self):
        if self.include_sections is None:
            self.include_sections = []

@dataclass
class ReportResult(BaseDomainModel):
    report_id: str = ""
    report_name: str = ""
    report_format: ReportFormat = ReportFormat.TXT
    output_path: str = ""
    created_at_utc: str = ""
    success: bool = False
    errors: list[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
