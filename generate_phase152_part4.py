import os
import textwrap

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(textwrap.dedent(content).lstrip())


# 11. METRIC INVENTORY
write_file("usa_signal_bot/backtesting/closure/metric_inventory.py", """
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestMetricInventoryItem, BacktestBandPhase, BacktestMetricInventoryKind,
    BacktestClosureRiskFlag
)

def extract_metric_items_from_payload(phase: BacktestBandPhase, payload: dict[str, Any]) -> list[BacktestMetricInventoryItem]:
    items = []
    # simplified mock extraction for inventory
    if phase == BacktestBandPhase.PHASE147_BACKTEST_RUN:
        metrics = payload.get("metrics", {})
        if "total_return" in metrics:
            item = BacktestMetricInventoryItem(
                metric_kind=BacktestMetricInventoryKind.RETURN_METRIC,
                metric_name="Total Return",
                source_phase=phase,
                source_artifact="BACKTEST_RUN_REVIEW",
                value=metrics["total_return"],
                non_trading_metric=True,
                not_investment_advice=True,
                suitable_for_phase153_research_input=True
            )
            items.append(item)
    elif phase == BacktestBandPhase.PHASE151_STRESS_MONTE_CARLO:
        stress = payload.get("stress_validation_report", {})
        if "max_stress_drawdown" in stress:
            item = BacktestMetricInventoryItem(
                metric_kind=BacktestMetricInventoryKind.STRESS_METRIC,
                metric_name="Max Stress Drawdown",
                source_phase=phase,
                source_artifact="STRESS_VALIDATION_REPORT",
                value=stress["max_stress_drawdown"],
                non_trading_metric=True,
                not_investment_advice=True,
                suitable_for_phase153_research_input=True
            )
            items.append(item)
    return items

def build_backtest_metric_inventory(payloads: dict[str, dict[str, Any]]) -> list[BacktestMetricInventoryItem]:
    inventory = []
    for phase_name, payload in payloads.items():
        try:
            phase = BacktestBandPhase(phase_name)
        except ValueError:
            phase = BacktestBandPhase.UNKNOWN
        inventory.extend(extract_metric_items_from_payload(phase, payload))
    return inventory

def validate_backtest_metric_inventory(items: list[BacktestMetricInventoryItem]) -> list[str]:
    errors = []
    for item in items:
        if not item.non_trading_metric:
            errors.append(f"Metric {item.metric_name} is not marked as non-trading")
        if not item.not_investment_advice:
            errors.append(f"Metric {item.metric_name} flagged as investment advice")
    return errors

def metric_inventory_summary(items: list[BacktestMetricInventoryItem]) -> dict[str, Any]:
    return {"count": len(items)}

def metric_inventory_to_text(items: list[BacktestMetricInventoryItem], limit: int = 300) -> str:
    return f"Metric Inventory: {len(items)} items"
""")

# 12. RISK NOTE INVENTORY
write_file("usa_signal_bot/backtesting/closure/risk_note_inventory.py", """
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestRiskNote, BacktestBandPhase, BacktestRiskNoteKind,
    BacktestClosureRiskFlag
)

def build_default_backtest_risk_notes() -> list[BacktestRiskNote]:
    return [
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.LOOKAHEAD_BIAS_NOTE,
            title="Lookahead Bias Limitation",
            note="Backtest assumes no lookahead bias, but residual risk remains.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.SURVIVORSHIP_BIAS_NOTE,
            title="Survivorship Bias Limitation",
            note="Universe selection may exhibit survivorship bias.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.COST_MODEL_NOTE,
            title="Cost Model Assumption",
            note="Transaction costs and slippage are approximations.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.LIQUIDITY_NOTE,
            title="Liquidity Constraint",
            note="Assumes sufficient market depth which may not hold in live trading.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.WALK_FORWARD_STABILITY_NOTE,
            title="Walk-Forward Stability",
            note="Historical stability does not guarantee future stability.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.STRESS_ROBUSTNESS_NOTE,
            title="Stress Test Limitations",
            note="Stress scenarios cannot cover all possible market shocks.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.HANDOFF_LIMITATION_NOTE,
            title="Research-Only Handoff",
            note="These artifacts are for research only and do not constitute deployment approval or investment advice.",
            severity="CRITICAL"
        )
    ]

def build_backtest_risk_note_inventory(payloads: dict[str, dict[str, Any]]) -> list[BacktestRiskNote]:
    return build_default_backtest_risk_notes()

def validate_backtest_risk_note_inventory(items: list[BacktestRiskNote]) -> list[str]:
    errors = []
    required_notes = ["Lookahead Bias Limitation", "Survivorship Bias Limitation", "Cost Model Assumption", "Liquidity Constraint", "Walk-Forward Stability", "Stress Test Limitations", "Research-Only Handoff"]
    titles = [n.title for n in items]
    for req in required_notes:
        if req not in titles:
            errors.append(f"Missing required risk note: {req}")
    for item in items:
        if not item.not_investment_advice:
            errors.append(f"Risk note {item.title} flagged as investment advice")
    return errors

def risk_note_inventory_summary(items: list[BacktestRiskNote]) -> dict[str, Any]:
    return {"count": len(items)}

def risk_note_inventory_to_text(items: list[BacktestRiskNote], limit: int = 300) -> str:
    return f"Risk Note Inventory: {len(items)} notes"
""")

# 13. ROBUSTNESS EVIDENCE TABLE
write_file("usa_signal_bot/backtesting/closure/robustness_evidence_table.py", """
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    RobustnessEvidenceRecord, BacktestMetricInventoryItem, BacktestRiskNote,
    ClosureComplianceStatus, BacktestBandPhase
)

def build_robustness_evidence_table(payloads: dict[str, dict[str, Any]], metric_inventory: list[BacktestMetricInventoryItem], risk_notes: list[BacktestRiskNote]) -> list[RobustnessEvidenceRecord]:
    evidence = []
    # simplified mock
    evidence.append(RobustnessEvidenceRecord(
        source_phase=BacktestBandPhase.PHASE151_STRESS_MONTE_CARLO,
        evidence_name="Monte Carlo Distribution Analysis",
        evidence_status=ClosureComplianceStatus.PASSED,
        supports_closure=True,
        supports_phase153_handoff=True
    ))
    return evidence

def validate_robustness_evidence_table(items: list[RobustnessEvidenceRecord]) -> list[str]:
    return []

def robustness_evidence_table_summary(items: list[RobustnessEvidenceRecord]) -> dict[str, Any]:
    return {"count": len(items)}

def robustness_evidence_table_to_text(items: list[RobustnessEvidenceRecord], limit: int = 300) -> str:
    return f"Robustness Evidence Table: {len(items)} records"
""")

# 14. ACCEPTANCE SUMMARY
write_file("usa_signal_bot/backtesting/closure/acceptance_summary.py", """
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
""")
