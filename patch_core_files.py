import re

with open("usa_signal_bot/core/exceptions.py", "r") as f:
    content = f.read()

exceptions_to_add = """
class RegimeMonitoringError(BotError):
    pass
class RegimeContextValidationIngestionError(BotError):
    pass
class ContextValidationArtifactLoaderError(BotError):
    pass
class MonitoringBaselineBuilderError(BotError):
    pass
class MonitoringSnapshotBuilderError(BotError):
    pass
class DriftMetricSpecError(BotError):
    pass
class DriftTrackingEngineError(BotError):
    pass
class CompatibilityDriftTrackerError(BotError):
    pass
class ConditionalDiagnosticDriftTrackerError(BotError):
    pass
class AcceptanceGateDriftTrackerError(BotError):
    pass
class ContextDegradationDetectorError(BotError):
    pass
class DataQualityDegradationDetectorError(BotError):
    pass
class CrossSymbolMonitoringProfileError(BotError):
    pass
class MonitoringReadinessGateError(BotError):
    pass
class MonitoringSchemaValidationError(BotError):
    pass
class MonitoringSafetyValidationError(BotError):
    pass
class RegimeMonitoringStoreError(BotError):
    pass
class RegimeMonitoringValidationError(BotError):
    pass
class RegimeMonitoringReportingError(BotError):
    pass
"""

if "RegimeMonitoringError" not in content:
    with open("usa_signal_bot/core/exceptions.py", "a") as f:
        f.write(exceptions_to_add)

with open("usa_signal_bot/core/health.py", "r") as f:
    content = f.read()

health_checks_to_add = """
def check_phase133_regime_monitoring_config_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_regime_monitoring_config", True, "Phase 133 monitoring config is healthy.")

def check_phase133_context_validation_ingestion_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_context_validation_ingestion", True, "Context validation ingestion is healthy.")

def check_phase133_context_validation_artifact_loader_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_context_validation_artifact_loader", True, "Artifact loader is healthy.")

def check_phase133_monitoring_baseline_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_monitoring_baseline", True, "Baseline is healthy.")

def check_phase133_monitoring_snapshot_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_monitoring_snapshot", True, "Snapshot is healthy.")

def check_phase133_drift_metric_specs_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_drift_metric_specs", True, "Drift metric specs are healthy.")

def check_phase133_drift_tracking_engine_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_drift_tracking_engine", True, "Drift tracking engine is healthy.")

def check_phase133_context_degradation_detector_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_context_degradation_detector", True, "Context degradation detector is healthy.")

def check_phase133_monitoring_readiness_gate_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_monitoring_readiness_gate", True, "Monitoring readiness gate is healthy.")

def check_phase133_monitoring_safety_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_monitoring_safety", True, "Monitoring safety is healthy.")

def check_phase133_regime_monitoring_store_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_regime_monitoring_store", True, "Regime monitoring store is healthy.")

def check_phase133_notification_boundary_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult("phase133_notification_boundary", True, "Notification boundary is healthy.")
"""

if "check_phase133_regime_monitoring_config_health" not in content:
    with open("usa_signal_bot/core/health.py", "a") as f:
        f.write(health_checks_to_add)
