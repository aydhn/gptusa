import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    ContextDegradationRule,
    ContextDegradationDiagnostic,
    ContextDegradationProfile,
    ContextDegradationKind,
    ContextDegradationStatus,
    RegimeDriftTrackingResult,
    RegimeDriftObservation,
    RegimeDriftSeverity,
    RegimeMonitoringQuality,
    create_context_degradation_rule_id,
    create_context_degradation_diagnostic_id,
    create_context_degradation_profile_id
)

def build_default_context_degradation_rules() -> List[ContextDegradationRule]:
    def _create_rule(name: str, kind: ContextDegradationKind) -> ContextDegradationRule:
        return ContextDegradationRule(
            rule_id=create_context_degradation_rule_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            degradation_kind=kind,
            name=name,
            warning_condition="drift_severity == HIGH",
            blocking_condition="drift_severity == BLOCKING",
            required=True,
            deterministic=True,
            research_metadata_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )

    return [
        _create_rule("Compatibility Score Degradation", ContextDegradationKind.COMPATIBILITY_DEGRADATION),
        _create_rule("Data Quality Degradation", ContextDegradationKind.DATA_QUALITY_DEGRADATION),
        _create_rule("Conditional Diagnostic Degradation", ContextDegradationKind.CONDITIONAL_DIAGNOSTIC_DEGRADATION),
        _create_rule("Acceptance Gate Degradation", ContextDegradationKind.ACCEPTANCE_GATE_DEGRADATION),
        _create_rule("Cross Symbol Degradation", ContextDegradationKind.CROSS_SYMBOL_DEGRADATION)
    ]

def infer_context_degradation_status(observation: RegimeDriftObservation) -> ContextDegradationStatus:
    if observation.drift_severity == RegimeDriftSeverity.BLOCKING:
        return ContextDegradationStatus.BLOCKED
    if observation.drift_severity == RegimeDriftSeverity.HIGH:
        return ContextDegradationStatus.DEGRADED
    if observation.drift_severity == RegimeDriftSeverity.MODERATE:
        return ContextDegradationStatus.WATCH
    return ContextDegradationStatus.NOT_DEGRADED

def build_degradation_diagnostic_from_observation(observation: RegimeDriftObservation, rule: ContextDegradationRule) -> ContextDegradationDiagnostic:
    status = infer_context_degradation_status(observation)
    recommended_action = "research_review"
    if status == ContextDegradationStatus.DEGRADED:
        recommended_action = "monitor_context"
    elif status == ContextDegradationStatus.BLOCKED:
        recommended_action = "baseline_refresh_review"

    return ContextDegradationDiagnostic(
        diagnostic_id=create_context_degradation_diagnostic_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        symbol=None,
        degradation_kind=rule.degradation_kind,
        status=status,
        severity=observation.drift_severity,
        source_observation_id=observation.observation_id,
        diagnostic_text=f"{rule.name} shows {status.value}",
        supporting_metrics={"absolute_change": observation.absolute_change, "relative_change": observation.relative_change},
        recommended_action_type=recommended_action,
        required_human_review=status in [ContextDegradationStatus.DEGRADED, ContextDegradationStatus.BLOCKED],
        research_metadata_only=True,
        investment_advice=False,
        activation_allowed=False,
        strategy_activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def detect_context_degradation(drift_result: RegimeDriftTrackingResult, rules: Optional[List[ContextDegradationRule]] = None) -> List[ContextDegradationDiagnostic]:
    rules = rules or build_default_context_degradation_rules()
    rule_map = {r.name: r for r in rules} # Simplified mapping, in reality would map properly
    # Using generic mapping for demo
    res = []
    for obs in drift_result.observations:
        # Simplistic rule matching
        rule = rules[0]
        if "data_quality" in obs.metric_name:
            rule = next((r for r in rules if r.degradation_kind == ContextDegradationKind.DATA_QUALITY_DEGRADATION), rules[0])
        elif "compatibility" in obs.metric_name:
            rule = next((r for r in rules if r.degradation_kind == ContextDegradationKind.COMPATIBILITY_DEGRADATION), rules[0])
        elif "diagnostic" in obs.metric_name or "context" in obs.metric_name:
             rule = next((r for r in rules if r.degradation_kind == ContextDegradationKind.CONDITIONAL_DIAGNOSTIC_DEGRADATION), rules[0])
        elif "acceptance_gate" in obs.metric_name:
             rule = next((r for r in rules if r.degradation_kind == ContextDegradationKind.ACCEPTANCE_GATE_DEGRADATION), rules[0])

        if obs.drift_severity != RegimeDriftSeverity.NONE:
            res.append(build_degradation_diagnostic_from_observation(obs, rule))
    return res

def build_context_degradation_profiles(items: List[ContextDegradationDiagnostic]) -> List[ContextDegradationProfile]:
    if not items:
        return []

    status = ContextDegradationStatus.NOT_DEGRADED
    if any(i.status == ContextDegradationStatus.BLOCKED for i in items):
        status = ContextDegradationStatus.BLOCKED
    elif any(i.status == ContextDegradationStatus.SEVERELY_DEGRADED for i in items):
        status = ContextDegradationStatus.SEVERELY_DEGRADED
    elif any(i.status == ContextDegradationStatus.DEGRADED for i in items):
        status = ContextDegradationStatus.DEGRADED
    elif any(i.status == ContextDegradationStatus.WATCH for i in items):
        status = ContextDegradationStatus.WATCH

    prof = ContextDegradationProfile(
        profile_id=create_context_degradation_profile_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        symbol=None,
        diagnostic_count=len(items),
        watch_count=sum(1 for i in items if i.status == ContextDegradationStatus.WATCH),
        degraded_count=sum(1 for i in items if i.status == ContextDegradationStatus.DEGRADED),
        severely_degraded_count=sum(1 for i in items if i.status == ContextDegradationStatus.SEVERELY_DEGRADED),
        blocked_count=sum(1 for i in items if i.status == ContextDegradationStatus.BLOCKED),
        profile_status=status,
        profile_summary=f"Overall status: {status.value}",
        quality=RegimeMonitoringQuality.HIGH if status == ContextDegradationStatus.NOT_DEGRADED else RegimeMonitoringQuality.WARNING,
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
    return [prof]

def validate_context_degradation_diagnostics(items: List[ContextDegradationDiagnostic]) -> List[str]:
    errors = []
    for item in items:
        if not item.research_metadata_only:
            errors.append(f"Diagnostic {item.diagnostic_id} not marked metadata_only")
        if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
            errors.append(f"Diagnostic {item.diagnostic_id} produces execution signal")
        if item.investment_advice:
            errors.append(f"Diagnostic {item.diagnostic_id} produces investment advice")
    return errors

def context_degradation_summary(items: List[ContextDegradationDiagnostic]) -> Dict[str, Any]:
    return {
        "count": len(items),
        "blocked": sum(1 for i in items if i.status == ContextDegradationStatus.BLOCKED)
    }

def context_degradation_to_text(items: List[ContextDegradationDiagnostic], limit: int = 300) -> str:
    summ = context_degradation_summary(items)
    text = f"Context Degradation: {summ}"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
