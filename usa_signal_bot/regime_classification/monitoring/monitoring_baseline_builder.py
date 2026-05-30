import datetime
import hashlib
import json
from typing import Any, Dict, List, Optional

from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringBaseline,
    RegimeMonitoringBaselineKind,
    create_regime_monitoring_baseline_id,
    RegimeMonitoringRiskFlag
)

def extract_baseline_metrics(compatibility_validation: Dict[str, Any], conditional_diagnostics: List[Dict[str, Any]], diagnostic_profiles: List[Dict[str, Any]], acceptance_gate: Dict[str, Any]) -> Dict[str, Any]:
    low_comp_count = sum(1 for c in compatibility_validation.get("symbol_results", []) if c.get("compatibility_category") == "LOW_COMPATIBILITY")
    uncertain_count = sum(1 for d in conditional_diagnostics if d.get("diagnostic_type") == "UNCERTAIN_CONTEXT")
    conflicted_count = sum(1 for d in conditional_diagnostics if d.get("diagnostic_type") == "CONFLICTED_CONTEXT")
    data_quality_count = sum(1 for d in conditional_diagnostics if d.get("diagnostic_type") == "DATA_QUALITY_LIMITED")

    return {
        "compatibility_result_count": len(compatibility_validation.get("symbol_results", [])),
        "conditional_diagnostic_count": len(conditional_diagnostics),
        "blocking_diagnostic_count": sum(1 for d in conditional_diagnostics if d.get("action") == "BLOCK"),
        "warning_diagnostic_count": sum(1 for d in conditional_diagnostics if d.get("action") == "WARN"),
        "acceptance_gate_status": acceptance_gate.get("status", "UNKNOWN"),
        "low_compatibility_count": low_comp_count,
        "uncertain_context_count": uncertain_count,
        "conflicted_context_count": conflicted_count,
        "data_quality_limited_count": data_quality_count
    }

def build_monitoring_baseline_from_payloads(
    source_review_id: Optional[str],
    compatibility_validation: Dict[str, Any],
    conditional_diagnostics: List[Dict[str, Any]],
    diagnostic_profiles: List[Dict[str, Any]],
    acceptance_gate: Dict[str, Any],
    baseline_version: str = "phase133.v1"
) -> RegimeMonitoringBaseline:

    metrics = extract_baseline_metrics(compatibility_validation, conditional_diagnostics, diagnostic_profiles, acceptance_gate)

    baseline = RegimeMonitoringBaseline(
        baseline_id=create_regime_monitoring_baseline_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        baseline_kind=RegimeMonitoringBaselineKind.COMBINED_BASELINE,
        source_review_id=source_review_id,
        baseline_version=baseline_version,
        baseline_hash=None,
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
        baseline_valid=True,
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
    baseline.baseline_hash = compute_monitoring_baseline_hash(baseline)
    return baseline

def compute_monitoring_baseline_hash(baseline: RegimeMonitoringBaseline) -> str:
    from usa_signal_bot.regime_classification.monitoring.phase133_models import regime_monitoring_baseline_to_dict
    d = regime_monitoring_baseline_to_dict(baseline)
    d.pop("baseline_hash", None)
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()

def validate_monitoring_baseline(baseline: RegimeMonitoringBaseline) -> List[str]:
    errors = []
    if not baseline.baseline_valid:
        errors.append("Baseline marked as invalid")
    if not baseline.research_metadata_only:
        errors.append("Baseline is not marked research_metadata_only")
    if baseline.produces_trade_signal or baseline.produces_order_decision or baseline.produces_portfolio_weights:
        errors.append("Baseline produces trade/order/portfolio output")
    if baseline.investment_advice:
        errors.append("Baseline produces investment advice")
    return errors

def monitoring_baseline_summary(baseline: RegimeMonitoringBaseline) -> Dict[str, Any]:
    return {
        "baseline_id": baseline.baseline_id,
        "valid": baseline.baseline_valid,
        "compatibility_count": baseline.compatibility_result_count,
        "diagnostic_count": baseline.conditional_diagnostic_count,
        "gate_status": baseline.acceptance_gate_status
    }

def monitoring_baseline_to_text(baseline: RegimeMonitoringBaseline, limit: int = 300) -> str:
    summ = monitoring_baseline_summary(baseline)
    text = f"Baseline: {summ}"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
