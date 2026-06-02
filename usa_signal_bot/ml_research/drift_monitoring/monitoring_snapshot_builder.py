from typing import Any, Dict, List, Optional
from .phase144_models import MonitoringSnapshotSpec, MonitoringWindowPolicy, DriftMetricResult
import uuid
import datetime

def create_monitoring_snapshot_spec_id() -> str:
    return f"mon_snap_{uuid.uuid4().hex[:12]}"

def build_monitoring_snapshot(policy: MonitoringWindowPolicy, baselines: List[Any], metrics: List[DriftMetricResult]) -> MonitoringSnapshotSpec:
    return MonitoringSnapshotSpec(snapshot_id=create_monitoring_snapshot_spec_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", snapshot_name="default", window_policy_id=policy.policy_id, drift_metric_result_ids=[], baseline_ids=[], snapshot_status=None, snapshot_hash=None, live_monitoring_enabled=False, alert_sender_enabled=False, dashboard_enabled=False, scheduler_enabled=False, daemon_started=False, research_data_only=True, warnings=[], errors=[], risk_flags=[], metadata={})

def compute_monitoring_snapshot_hash(snapshot: MonitoringSnapshotSpec) -> str:
    return ""

def validate_monitoring_snapshot(snapshot: MonitoringSnapshotSpec) -> List[str]:
    return []

def monitoring_snapshot_summary(snapshot: MonitoringSnapshotSpec) -> Dict[str, Any]:
    return {}

def monitoring_snapshot_to_text(snapshot: MonitoringSnapshotSpec, limit: int = 300) -> str:
    return "Snapshot"
