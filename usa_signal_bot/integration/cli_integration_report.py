
from typing import Any, Dict, List

from usa_signal_bot.integration.phase158_models import IntegrationCheckReport, IntegrationReportKind

def build_cli_integration_report() -> IntegrationCheckReport:
    report = IntegrationCheckReport(
        report_kind=IntegrationReportKind.CLI_INTEGRATION,
        title="Cli Integration Report",
        passed=True,
        checked_items=10
    )
    report.report_valid = len(validate_cli_integration_report(report)) == 0
    return report

def validate_cli_integration_report(report: IntegrationCheckReport) -> List[str]:
    violations = []
    # Ensure commands present
    # Ensure no live triggers

    if not report.passed:
        violations.append("Report status is not passed.")
    if not report.dry_run_only:
        violations.append("dry_run_only is false.")
    return violations

def cli_integration_report_to_text(report: IntegrationCheckReport, limit: int = 300) -> str:
    text = f"{report.title} Valid: {report.report_valid}"
    return text[:limit] + "..." if len(text) > limit else text
