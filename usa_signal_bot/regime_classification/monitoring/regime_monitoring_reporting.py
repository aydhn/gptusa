from typing import Any, Dict
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeContextValidationIngestionResult,
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    RegimeDriftMetricSpec,
    RegimeDriftObservation,
    RegimeDriftTrackingResult,
    ContextDegradationRule,
    ContextDegradationDiagnostic,
    ContextDegradationProfile,
    RegimeMonitoringReadinessGate,
    RegimeMonitoringContext,
    RegimeMonitoringFullReview
)
from usa_signal_bot.regime_classification.monitoring.regime_context_validation_ingestion import regime_context_validation_ingestion_to_text
from usa_signal_bot.regime_classification.monitoring.monitoring_baseline_builder import monitoring_baseline_to_text
from usa_signal_bot.regime_classification.monitoring.monitoring_snapshot_builder import monitoring_snapshot_to_text
from usa_signal_bot.regime_classification.monitoring.drift_metric_specs import drift_metric_specs_to_text
from usa_signal_bot.regime_classification.monitoring.drift_tracking_engine import drift_tracking_to_text
from usa_signal_bot.regime_classification.monitoring.context_degradation_detector import context_degradation_to_text
from usa_signal_bot.regime_classification.monitoring.cross_symbol_monitoring_profiles import cross_symbol_monitoring_to_text
from usa_signal_bot.regime_classification.monitoring.monitoring_readiness_gate import regime_monitoring_readiness_gate_to_text
from usa_signal_bot.regime_classification.monitoring.regime_monitoring_report import regime_monitoring_full_review_to_text, regime_monitoring_limitations_text

def regime_context_validation_ingestion_result_to_text(item: RegimeContextValidationIngestionResult) -> str:
    return regime_context_validation_ingestion_to_text(item)

def regime_monitoring_baseline_to_text(item: RegimeMonitoringBaseline, limit: int = 300) -> str:
    return monitoring_baseline_to_text(item, limit)

def regime_monitoring_snapshot_to_text(item: RegimeMonitoringSnapshot, limit: int = 300) -> str:
    return monitoring_snapshot_to_text(item, limit)

def regime_drift_metric_spec_to_text(item: RegimeDriftMetricSpec) -> str:
    return f"Drift Spec: {item.metric_name}"

def regime_drift_observation_to_text(item: RegimeDriftObservation) -> str:
    return f"Observation: {item.metric_name} -> {item.drift_severity.value}"

def regime_drift_tracking_result_to_text(item: RegimeDriftTrackingResult, limit: int = 300) -> str:
    return drift_tracking_to_text(item, limit)

def context_degradation_rule_to_text(item: ContextDegradationRule) -> str:
    return f"Degradation Rule: {item.name}"

def context_degradation_diagnostic_to_text(item: ContextDegradationDiagnostic) -> str:
    return f"Diagnostic: {item.diagnostic_text}"

def context_degradation_profile_to_text(item: ContextDegradationProfile) -> str:
    return cross_symbol_monitoring_to_text(item)

def regime_monitoring_context_to_text(item: RegimeMonitoringContext, limit: int = 300) -> str:
    return f"Monitoring Context: {item.status.value}"

def regime_monitoring_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
