from dataclasses import dataclass, field
from typing import Any, List, Dict
import json
import re

from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    SymbolLifecycleRecord, SymbolAliasRecord, UniverseSnapshot,
    SymbolHistoryCheck, SurvivorshipBiasAssessment, UniverseLifecycleReviewResult
)
from usa_signal_bot.core.exceptions import LifecycleValidationError

@dataclass
class LifecycleValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LifecycleValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[LifecycleValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[LifecycleValidationIssue]) -> LifecycleValidationReport:
    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    blocked = [i.message for i in issues if i.severity == "BLOCKER"]
    return LifecycleValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_lifecycle_registry_report(records: List[SymbolLifecycleRecord]) -> LifecycleValidationReport:
    issues = []
    seen = set()
    for r in records:
        if not r.symbol:
            issues.append(LifecycleValidationIssue("ERROR", "symbol", "Empty symbol in registry."))
        if r.symbol in seen:
            issues.append(LifecycleValidationIssue("WARNING", "symbol", f"Duplicate symbol in registry: {r.symbol}"))
        seen.add(r.symbol)
        if r.listed_date and r.delisted_date and r.delisted_date < r.listed_date:
            issues.append(LifecycleValidationIssue("ERROR", "delisted_date", f"Invalid dates for {r.symbol}: delisted before listed."))
    return _create_report(issues)

def validate_symbol_aliases_report(aliases: List[SymbolAliasRecord]) -> LifecycleValidationReport:
    issues = []
    seen = set()
    for a in aliases:
        if not a.old_symbol or not a.new_symbol:
            issues.append(LifecycleValidationIssue("ERROR", "symbols", "Empty symbol in alias."))
        if a.old_symbol in seen:
             issues.append(LifecycleValidationIssue("WARNING", "old_symbol", f"Multiple aliases for {a.old_symbol}."))
        seen.add(a.old_symbol)
        if a.old_symbol == a.new_symbol:
            issues.append(LifecycleValidationIssue("ERROR", "symbols", f"Alias loops to self: {a.old_symbol}"))
    return _create_report(issues)

def validate_universe_snapshot_report(snapshot: UniverseSnapshot) -> LifecycleValidationReport:
    issues = []
    if snapshot.symbol_count != len(snapshot.symbols):
        issues.append(LifecycleValidationIssue("ERROR", "symbol_count", "Symbol count mismatch."))
    return _create_report(issues)

def validate_symbol_history_checks_report(checks: List[SymbolHistoryCheck]) -> LifecycleValidationReport:
    issues = []
    for c in checks:
        if not c.symbol:
            issues.append(LifecycleValidationIssue("ERROR", "symbol", "Empty symbol in history check."))
    return _create_report(issues)

def validate_survivorship_assessment_report(assessment: SurvivorshipBiasAssessment) -> LifecycleValidationReport:
    issues = []
    if assessment.delisted_symbol_count > assessment.current_symbol_count:
        issues.append(LifecycleValidationIssue("ERROR", "counts", "Delisted count exceeds total current count."))
    return _create_report(issues)

def validate_universe_lifecycle_review_report(result: UniverseLifecycleReviewResult) -> LifecycleValidationReport:
    issues = []
    r1 = validate_lifecycle_registry_report(result.lifecycle_records)
    r2 = validate_symbol_aliases_report(result.aliases)
    issues.extend(r1.issues)
    issues.extend(r2.issues)
    return _create_report(issues)

def validate_no_sensitive_data_in_lifecycle_payload(payload: Dict[str, Any]) -> LifecycleValidationReport:
    issues = []
    text = json.dumps(payload).lower()
    if re.search(r'(api_key|token|secret|password)', text):
        issues.append(LifecycleValidationIssue("ERROR", "payload", "Potential sensitive data leak detected."))
    return _create_report(issues)

def validate_no_live_execution_language_in_lifecycle(text: str) -> LifecycleValidationReport:
    issues = []
    t = text.lower()
    bad_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "investment advice"]
    for p in bad_phrases:
        if p in t:
            issues.append(LifecycleValidationIssue("ERROR", "text", f"Prohibited language detected: '{p}'"))
    return _create_report(issues)

def lifecycle_validation_report_to_text(report: LifecycleValidationReport) -> str:
    lines = [f"Validation Valid: {report.valid}"]
    lines.append(f"Issues: {report.issue_count} (E:{report.error_count}, W:{report.warning_count}, B:{report.blocked_count})")
    for i in report.issues:
        lines.append(f" [{i.severity}] {i.field}: {i.message}")
    return "\n".join(lines)

def assert_lifecycle_valid(report: LifecycleValidationReport) -> None:
    if not report.valid:
        raise LifecycleValidationError(f"Lifecycle validation failed: {report.errors}")
