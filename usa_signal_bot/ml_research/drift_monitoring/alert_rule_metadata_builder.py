from typing import Any, Dict, List, Optional
from .phase144_models import DriftAlertRuleMetadata, DriftMetricResult
import uuid
import datetime

def create_drift_alert_rule_metadata_id() -> str:
    return f"alert_rule_{uuid.uuid4().hex[:12]}"

def build_default_drift_alert_rule_metadata(metrics: List[DriftMetricResult]) -> List[DriftAlertRuleMetadata]:
    return []

def build_alert_rule_for_metric(metric: DriftMetricResult) -> DriftAlertRuleMetadata:
    return DriftAlertRuleMetadata(rule_id=create_drift_alert_rule_metadata_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", rule_name="rule", baseline_kind=metric.baseline_kind, metric_kind=metric.metric_kind, severity_trigger=None, threshold_metadata={}, notification_preview_only=True, alert_sender_enabled=False, telegram_real_send_enabled=False, scheduler_enabled=False, daemon_started=False, rule_status=None, rule_hash=None, research_data_only=True, warnings=[], errors=[], risk_flags=[], metadata={})

def compute_alert_rule_hash(rule: DriftAlertRuleMetadata) -> str:
    return ""

def validate_alert_rule_metadata(items: List[DriftAlertRuleMetadata]) -> List[str]:
    return []

def alert_rule_metadata_summary(items: List[DriftAlertRuleMetadata]) -> Dict[str, Any]:
    return {}

def alert_rule_metadata_to_text(items: List[DriftAlertRuleMetadata], limit: int = 300) -> str:
    return "Alert rules"
