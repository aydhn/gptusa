from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    AcceptanceSummary, ArtifactAvailabilityAudit, DeterminismComplianceAudit,
    SafetyComplianceAudit, ResearchBoundaryAudit, RobustnessEvidenceRecord,
    BacktestClosureQuality, ClosureComplianceStatus
)

def build_acceptance_summary(availability: ArtifactAvailabilityAudit, determinism: DeterminismComplianceAudit, safety: SafetyComplianceAudit, research: ResearchBoundaryAudit, evidence: list[RobustnessEvidenceRecord]) -> AcceptanceSummary:
    summary = AcceptanceSummary()

    all_checks = availability.checks + determinism.checks + safety.checks + research.checks
    summary.checks = all_checks

    summary.passed_count = sum(1 for c in all_checks if c.status == ClosureComplianceStatus.PASSED)
    summary.warning_count = sum(1 for c in all_checks if c.status == ClosureComplianceStatus.WARNING)
    summary.failed_count = sum(1 for c in all_checks if c.status == ClosureComplianceStatus.FAILED)
    summary.blocked_count = sum(1 for c in all_checks if c.status == ClosureComplianceStatus.BLOCKED)

    summary.acceptance_passed = availability.audit_passed and determinism.audit_passed and safety.audit_passed and research.audit_passed
    summary.quality = infer_backtest_closure_quality(summary)

    return summary

def infer_backtest_closure_quality(summary: AcceptanceSummary) -> BacktestClosureQuality:
    if not summary.acceptance_passed:
        return BacktestClosureQuality.BLOCKED if summary.blocked_count > 0 else BacktestClosureQuality.INVALID
    if summary.failed_count > 0:
        return BacktestClosureQuality.INVALID
    if summary.warning_count > 0:
        return BacktestClosureQuality.WARNING
    return BacktestClosureQuality.HIGH

def validate_acceptance_summary(summary: AcceptanceSummary) -> list[str]:
    errors = []
    if not summary.acceptance_passed:
        errors.append("Acceptance summary failed")
    return errors

def acceptance_summary_to_text(summary: AcceptanceSummary, limit: int = 300) -> str:
    return f"AcceptanceSummary(passed={summary.acceptance_passed}, quality={summary.quality.value}, passed_checks={summary.passed_count})"
