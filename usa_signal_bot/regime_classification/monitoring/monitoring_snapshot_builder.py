import datetime
import hashlib
import json
from typing import Any, Dict, List, Optional

from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringSnapshot,
    RegimeMonitoringSnapshotKind,
    create_regime_monitoring_snapshot_id,
    RegimeMonitoringRiskFlag
)
from usa_signal_bot.regime_classification.monitoring.monitoring_baseline_builder import extract_baseline_metrics

def extract_snapshot_metrics(compatibility_validation: Dict[str, Any], conditional_diagnostics: List[Dict[str, Any]], diagnostic_profiles: List[Dict[str, Any]], acceptance_gate: Dict[str, Any]) -> Dict[str, Any]:
    return extract_baseline_metrics(compatibility_validation, conditional_diagnostics, diagnostic_profiles, acceptance_gate)

def build_monitoring_snapshot_from_payloads(
    source_review_id: Optional[str],
    compatibility_validation: Dict[str, Any],
    conditional_diagnostics: List[Dict[str, Any]],
    diagnostic_profiles: List[Dict[str, Any]],
    acceptance_gate: Dict[str, Any],
    snapshot_kind: RegimeMonitoringSnapshotKind = RegimeMonitoringSnapshotKind.CURRENT_CONTEXT_VALIDATION_SNAPSHOT
) -> RegimeMonitoringSnapshot:

    metrics = extract_snapshot_metrics(compatibility_validation, conditional_diagnostics, diagnostic_profiles, acceptance_gate)

    snapshot = RegimeMonitoringSnapshot(
        snapshot_id=create_regime_monitoring_snapshot_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        snapshot_kind=snapshot_kind,
        source_review_id=source_review_id,
        snapshot_hash=None,
        compatibility_result_count=metrics["compatibility_result_count"],
        conditional_diagnostic_count=metrics["conditional_diagnostic_count"],
        blocking_diagnostic_count=metrics["blocking_diagnostic_count"],
        warning_diagnostic_count=metrics["warning_diagnostic_count"],
        acceptance_gate_status=metrics["acceptance_gate_status"],
        low_compatibility_count=metrics["low_compatibility_count"],
        uncertain_context_count=metrics["uncertain_context_count"],
        conflicted_context_count=metrics["conflicted_context_count"],
        data_quality_limited_count=metrics["data_quality_limited_count"],
        cross_symbol_summary={"profile_count": len(diagnostic_profiles)},
        metrics=metrics,
        snapshot_valid=True,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    snapshot.snapshot_hash = compute_monitoring_snapshot_hash(snapshot)
    return snapshot

def compute_monitoring_snapshot_hash(snapshot: RegimeMonitoringSnapshot) -> str:
    from usa_signal_bot.regime_classification.monitoring.phase133_models import regime_monitoring_snapshot_to_dict
    d = regime_monitoring_snapshot_to_dict(snapshot)
    d.pop("snapshot_hash", None)
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()

def validate_monitoring_snapshot(snapshot: RegimeMonitoringSnapshot) -> List[str]:
    errors = []
    if not snapshot.snapshot_valid:
        errors.append("Snapshot marked as invalid")
    if not snapshot.research_metadata_only:
        errors.append("Snapshot is not marked research_metadata_only")
    if snapshot.produces_trade_signal or snapshot.produces_order_decision or snapshot.produces_portfolio_weights:
        errors.append("Snapshot produces trade/order/portfolio output")
    if snapshot.investment_advice:
        errors.append("Snapshot produces investment advice")
    return errors

def monitoring_snapshot_summary(snapshot: RegimeMonitoringSnapshot) -> Dict[str, Any]:
    return {
        "snapshot_id": snapshot.snapshot_id,
        "valid": snapshot.snapshot_valid,
        "compatibility_count": snapshot.compatibility_result_count,
        "diagnostic_count": snapshot.conditional_diagnostic_count,
        "gate_status": snapshot.acceptance_gate_status
    }

def monitoring_snapshot_to_text(snapshot: RegimeMonitoringSnapshot, limit: int = 300) -> str:
    summ = monitoring_snapshot_summary(snapshot)
    text = f"Snapshot: {summ}"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
