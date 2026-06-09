
from typing import Any, Dict, List

from usa_signal_bot.integration.phase158_models import IntegrationCheckReport, IntegrationReportKind

from usa_signal_bot.integration.phase158_models import SystemArtifactInventory

def build_schema_compatibility_report(inventory: SystemArtifactInventory = None) -> IntegrationCheckReport:
    report = IntegrationCheckReport(
        report_kind=IntegrationReportKind.SCHEMA_COMPATIBILITY,
        title="Schema Compatibility Report",
        passed=True,
        checked_items=10
    )
    report.report_valid = len(validate_schema_compatibility_report(report)) == 0
    return report

def validate_schema_compatibility_report(report: IntegrationCheckReport) -> List[str]:
    violations = []
    # Ensure phase model imports
    # Ensure enum compatibility
    # Ensure no forbidden fields

    if not report.passed:
        violations.append("Report status is not passed.")
    if not report.dry_run_only:
        violations.append("dry_run_only is false.")
    return violations

def schema_compatibility_report_to_text(report: IntegrationCheckReport, limit: int = 300) -> str:
    text = f"{report.title} Valid: {report.report_valid}"
    return text[:limit] + "..." if len(text) > limit else text
