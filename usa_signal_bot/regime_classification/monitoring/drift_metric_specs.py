import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeDriftMetricSpec,
    RegimeDriftMetricKind,
    create_regime_drift_metric_spec_id
)

def build_default_drift_metric_specs() -> List[RegimeDriftMetricSpec]:
    def _create_spec(name: str, kind: RegimeDriftMetricKind, higher_is_worse: bool, warning_th: float, blocking_th: float) -> RegimeDriftMetricSpec:
        return RegimeDriftMetricSpec(
            spec_id=create_regime_drift_metric_spec_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            metric_name=name,
            metric_kind=kind,
            baseline_field=name,
            snapshot_field=name,
            warning_threshold=warning_th,
            blocking_threshold=blocking_th,
            higher_is_worse=higher_is_worse,
            deterministic=True,
            research_metadata_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )

    return [
        _create_spec("compatibility_result_count", RegimeDriftMetricKind.COMPATIBILITY_SCORE_DRIFT, False, 10.0, 25.0),
        _create_spec("low_compatibility_count", RegimeDriftMetricKind.LOW_COMPATIBILITY_COUNT_DRIFT, True, 5.0, 15.0),
        _create_spec("uncertain_context_count", RegimeDriftMetricKind.UNCERTAIN_CONTEXT_COUNT_DRIFT, True, 5.0, 15.0),
        _create_spec("conflicted_context_count", RegimeDriftMetricKind.CONFLICTED_CONTEXT_COUNT_DRIFT, True, 5.0, 15.0),
        _create_spec("data_quality_limited_count", RegimeDriftMetricKind.DATA_QUALITY_LIMITED_COUNT_DRIFT, True, 5.0, 15.0),
        _create_spec("warning_diagnostic_count", RegimeDriftMetricKind.CONDITIONAL_WARNING_COUNT_DRIFT, True, 10.0, 25.0),
        _create_spec("blocking_diagnostic_count", RegimeDriftMetricKind.CONDITIONAL_BLOCKING_COUNT_DRIFT, True, 5.0, 15.0),
        _create_spec("acceptance_gate_status", RegimeDriftMetricKind.ACCEPTANCE_GATE_STATUS_DRIFT, False, 0.0, 0.0),
        _create_spec("cross_symbol_distribution", RegimeDriftMetricKind.CROSS_SYMBOL_DISTRIBUTION_DRIFT, False, 10.0, 25.0),
    ]

def drift_metric_spec_by_name(name: str, specs: Optional[List[RegimeDriftMetricSpec]] = None) -> Optional[RegimeDriftMetricSpec]:
    specs = specs or build_default_drift_metric_specs()
    for s in specs:
        if s.metric_name == name:
            return s
    return None

def validate_drift_metric_specs(specs: List[RegimeDriftMetricSpec]) -> List[str]:
    errors = []
    names = set()
    for s in specs:
        if s.metric_name in names:
            errors.append(f"Duplicate spec name: {s.metric_name}")
        names.add(s.metric_name)
    return errors

def drift_metric_specs_summary(specs: List[RegimeDriftMetricSpec]) -> Dict[str, Any]:
    return {
        "count": len(specs),
        "names": [s.metric_name for s in specs]
    }

def drift_metric_specs_to_text(specs: List[RegimeDriftMetricSpec], limit: int = 200) -> str:
    summ = drift_metric_specs_summary(specs)
    text = f"Specs Summary: {summ}"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
