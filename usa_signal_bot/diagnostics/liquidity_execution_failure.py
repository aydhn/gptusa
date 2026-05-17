from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, create_failure_mode_assessment_id
)
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope
from datetime import datetime, timezone

def identify_liquidity_failure_events(events: List[DiagnosticEvent]) -> List[DiagnosticEvent]:
    failures = []
    for e in events:
        bucket = e.liquidity_bucket or ""
        if bucket.lower() in ["thin", "illiquid", "low_liquidity"] and e.net_pnl_usd is not None and e.net_pnl_usd < 0:
            failures.append(e)
    return failures

def identify_execution_cost_failure_events(events: List[DiagnosticEvent]) -> List[DiagnosticEvent]:
    failures = []
    for e in events:
        bucket = e.cost_bucket or ""
        if bucket.lower() in ["high_cost", "high_impact", "high_slippage"] and e.net_pnl_usd is not None and e.net_pnl_usd < 0:
            failures.append(e)
    return failures

def liquidity_failure_assessments(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    failures = identify_liquidity_failure_events(events)
    grouped = {}
    for e in failures:
        symbol = e.symbol or "UNKNOWN"
        if symbol not in grouped:
            grouped[symbol] = []
        grouped[symbol].append(e)

    assessments = []
    for symbol, group in grouped.items():
        total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.LOW_LIQUIDITY),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.LOW_LIQUIDITY,
            severity=DiagnosticSeverity.MODERATE if len(group) >= 3 else DiagnosticSeverity.LOW,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 3 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.SYMBOL,
            affected_name=symbol,
            event_count=len(group),
            loss_count=len(group),
            total_net_loss_usd=total_loss,
            evidence={"liquidity_bucket": "low_liquidity"}
        ))
    return assessments

def execution_failure_assessments(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    failures = identify_execution_cost_failure_events(events)
    grouped = {}
    for e in failures:
        symbol = e.symbol or "UNKNOWN"
        if symbol not in grouped:
            grouped[symbol] = []
        grouped[symbol].append(e)

    assessments = []
    for symbol, group in grouped.items():
        total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.HIGH_SLIPPAGE),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.HIGH_SLIPPAGE,
            severity=DiagnosticSeverity.MODERATE if len(group) >= 3 else DiagnosticSeverity.LOW,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 3 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.SYMBOL,
            affected_name=symbol,
            event_count=len(group),
            loss_count=len(group),
            total_net_loss_usd=total_loss,
            evidence={"cost_bucket": "high_cost"}
        ))
    return assessments

def liquidity_execution_failure_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    liq_fails = identify_liquidity_failure_events(events)
    exec_fails = identify_execution_cost_failure_events(events)
    return {
        "liquidity_failure_count": len(liq_fails),
        "execution_failure_count": len(exec_fails)
    }

def liquidity_execution_failure_to_text(payload: Dict[str, Any]) -> str:
    lines = [
        "Liquidity & Execution Failure Summary:",
        f"  Liquidity Failures: {payload.get('liquidity_failure_count', 0)}",
        f"  Execution Failures: {payload.get('execution_failure_count', 0)}"
    ]
    return "\n".join(lines)
