import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- portfolio_construction/construction_validation.py ---
val_code = """from dataclasses import dataclass, field
from typing import Any
import json

from usa_signal_bot.portfolio_construction.portfolio_models import (
    SectorClusterRecord, ExposureSnapshot, ConcentrationAssessment,
    PortfolioConstructionPlan, PortfolioConstructionReview,
    validate_sector_cluster_record, validate_exposure_snapshot,
    validate_concentration_assessment, validate_portfolio_candidate,
    validate_portfolio_allocation
)

@dataclass
class PortfolioConstructionValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioConstructionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[PortfolioConstructionValidationIssue]
    warnings: list[str]
    errors: list[str]

def _build_report(issues: list[PortfolioConstructionValidationIssue]) -> PortfolioConstructionValidationReport:
    errors = [i for i in issues if i.severity == "ERROR"]
    warnings = [i for i in issues if i.severity == "WARNING"]
    return PortfolioConstructionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[w.message for w in warnings],
        errors=[e.message for e in errors]
    )

def validate_sector_cluster_records_report(items: list[SectorClusterRecord]) -> PortfolioConstructionValidationReport:
    issues = []
    for item in items:
        try:
            validate_sector_cluster_record(item)
        except ValueError as e:
            issues.append(PortfolioConstructionValidationIssue("ERROR", "symbol", str(e)))
    return _build_report(issues)

def validate_exposure_snapshot_report(item: ExposureSnapshot) -> PortfolioConstructionValidationReport:
    issues = []
    try:
        validate_exposure_snapshot(item)
    except ValueError as e:
        issues.append(PortfolioConstructionValidationIssue("ERROR", "exposure", str(e)))
    return _build_report(issues)

def validate_concentration_assessments_report(items: list[ConcentrationAssessment]) -> PortfolioConstructionValidationReport:
    issues = []
    for item in items:
        try:
            validate_concentration_assessment(item)
        except ValueError as e:
            issues.append(PortfolioConstructionValidationIssue("ERROR", "assessment", str(e)))
    return _build_report(issues)

def validate_portfolio_construction_plan_report(item: PortfolioConstructionPlan) -> PortfolioConstructionValidationReport:
    issues = []
    for c in item.candidates:
        try:
            validate_portfolio_candidate(c)
        except ValueError as e:
            issues.append(PortfolioConstructionValidationIssue("ERROR", "candidate", str(e)))
    for a in item.allocations:
        try:
            validate_portfolio_allocation(a)
        except ValueError as e:
            issues.append(PortfolioConstructionValidationIssue("ERROR", "allocation", str(e)))
    if item.total_allocated_notional_usd and item.exposure_snapshot and item.exposure_snapshot.total_equity_usd:
        if item.total_allocated_notional_usd > item.exposure_snapshot.total_equity_usd:
             issues.append(PortfolioConstructionValidationIssue("WARNING", "total_allocated", "Total allocated exceeds total equity"))
    return _build_report(issues)

def validate_portfolio_construction_review_report(item: PortfolioConstructionReview) -> PortfolioConstructionValidationReport:
    issues = []
    if item.plan:
        res = validate_portfolio_construction_plan_report(item.plan)
        issues.extend(res.issues)
    if item.exposure_snapshot:
        res = validate_exposure_snapshot_report(item.exposure_snapshot)
        issues.extend(res.issues)
    return _build_report(issues)

def validate_no_live_execution_language_in_portfolio(text: str) -> PortfolioConstructionValidationReport:
    issues = []
    lower_text = text.lower()
    banned_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "kesin kar", "kesin portföy", "bu portföy kesin alınmalı", "investment advice", "optimal portfolio"]
    for phrase in banned_phrases:
        if phrase in lower_text:
            issues.append(PortfolioConstructionValidationIssue("ERROR", "language", f"Banned phrase found: {phrase}"))
    return _build_report(issues)

def validate_no_broker_execution_fields_in_portfolio(payload: dict[str, Any]) -> PortfolioConstructionValidationReport:
    issues = []
    banned_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    payload_str = json.dumps(payload).lower()
    for f in banned_fields:
        if f in payload_str:
            issues.append(PortfolioConstructionValidationIssue("ERROR", "fields", f"Banned broker field found: {f}"))
    return _build_report(issues)

def validate_no_sensitive_data_in_portfolio_payload(payload: dict[str, Any]) -> PortfolioConstructionValidationReport:
    issues = []
    banned = ["api_key", "secret", "token", "password"]
    payload_str = json.dumps(payload).lower()
    for f in banned:
        if f in payload_str:
            issues.append(PortfolioConstructionValidationIssue("ERROR", "security", f"Potential secret leak found: {f}"))
    return _build_report(issues)

def portfolio_construction_validation_report_to_text(report: PortfolioConstructionValidationReport) -> str:
    lines = [f"Validation Report (Valid: {report.valid})"]
    lines.append(f"Errors: {report.error_count}, Warnings: {report.warning_count}")
    for i in report.issues:
        lines.append(f"  [{i.severity}] {i.field}: {i.message}")
    return "\\n".join(lines)

def assert_portfolio_construction_valid(report: PortfolioConstructionValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Portfolio Construction Validation failed: {report.errors}")
"""
write_file("usa_signal_bot/portfolio_construction/construction_validation.py", val_code)


# --- portfolio_construction/construction_reporting.py ---
rep_code = """from usa_signal_bot.portfolio_construction.portfolio_models import (
    SectorClusterRecord, ExposureSnapshot, ConcentrationAssessment,
    PortfolioAllocation, PortfolioCandidate, PortfolioConstructionPlan, PortfolioConstructionReview
)

def sector_cluster_record_to_text(item: SectorClusterRecord) -> str:
    return f"{item.symbol}: Sector={item.sector}, Cluster={item.cluster}"

def portfolio_candidate_to_text(item: PortfolioCandidate) -> str:
    return f"{item.symbol}: Score={item.score}, Conf={item.confidence}, Sector={item.sector}"

def exposure_snapshot_to_text(item: ExposureSnapshot) -> str:
    lines = [f"Exposure Snapshot ({item.snapshot_id})"]
    lines.append(f"  Gross: ${item.gross_exposure_usd:.2f}, Net: ${item.net_exposure_usd:.2f}")
    return "\\n".join(lines)

def concentration_assessment_to_text(item: ConcentrationAssessment) -> str:
    return f"{item.name} ({item.exposure_type.value if hasattr(item.exposure_type, 'value') else str(item.exposure_type)}): {item.exposure_pct_equity}% vs {item.limit_pct_equity}% -> {item.decision.value if hasattr(item.decision, 'value') else str(item.decision)}"

def portfolio_allocation_to_text(item: PortfolioAllocation) -> str:
    return f"{item.symbol}: {item.weight_pct_equity}% (${item.final_notional_usd}) -> {item.status.value if hasattr(item.status, 'value') else str(item.status)}"

def portfolio_construction_plan_to_text(item: PortfolioConstructionPlan, limit: int = 100) -> str:
    lines = [f"Portfolio Construction Plan ({item.plan_id})", f"Mode: {item.mode.value if hasattr(item.mode, 'value') else str(item.mode)}"]
    lines.append(f"Allocations ({item.approved_count} approved, {item.reduced_count} reduced, {item.suppressed_count} suppressed):")
    for a in item.allocations[:limit]:
        lines.append("  " + portfolio_allocation_to_text(a))
    return "\\n".join(lines)

def portfolio_construction_review_to_text(item: PortfolioConstructionReview, limit: int = 100) -> str:
    lines = [f"Portfolio Construction Review ({item.review_id})"]
    if item.plan:
        lines.append(portfolio_construction_plan_to_text(item.plan, limit))
    if item.exposure_snapshot:
        lines.append(exposure_snapshot_to_text(item.exposure_snapshot))
    lines.append(portfolio_construction_limitations_text())
    return "\\n".join(lines)

def construction_store_summary_to_text(summary: dict[str, any]) -> str:
    lines = ["Construction Store Summary"]
    for k, v in summary.items():
        lines.append(f"  {k}: {v}")
    return "\\n".join(lines)

def portfolio_construction_limitations_text() -> str:
    return (
        "\\n=== PORTFOLIO CONSTRUCTION LIMITATIONS ===\\n"
        "1. This is a local metadata layer and NOT an official broker portfolio.\\n"
        "2. Sector/cluster mappings are local heuristics/proxies, not official classifications.\\n"
        "3. Correlation proxies are rough heuristics, not true statistical correlations.\\n"
        "4. This plan is NOT investment advice and makes no claims of future profitability.\\n"
        "5. 'APPROVED' or 'PASS' status is NOT an authorization for live trading.\\n"
        "6. No real or demo broker orders are generated by this system."
    )
"""
write_file("usa_signal_bot/portfolio_construction/construction_reporting.py", rep_code)

print("Generated step 6")
