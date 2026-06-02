from typing import Any, Dict, List, Optional
from .phase144_models import MonitoringWindowPolicy, MonitoringWindowKind
import uuid
import datetime

def create_monitoring_window_policy_id() -> str:
    return f"window_pol_{uuid.uuid4().hex[:12]}"

def build_default_monitoring_window_policy(reference_splits: Optional[List[str]] = None, monitoring_splits: Optional[List[str]] = None) -> MonitoringWindowPolicy:
    if reference_splits is None:
        reference_splits = ["train", "validation"]
    if monitoring_splits is None:
        monitoring_splits = ["test"]

    return MonitoringWindowPolicy(
        policy_id=create_monitoring_window_policy_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        policy_name="default_window_policy",
        reference_window_kind=MonitoringWindowKind.TRAIN_REFERENCE_WINDOW,
        monitoring_window_kind=MonitoringWindowKind.TEST_REFERENCE_WINDOW,
        reference_split_names=reference_splits,
        monitoring_split_names=monitoring_splits,
        min_reference_rows=10,
        min_monitoring_rows=5,
        rolling_window_size=None,
        calendar_window_label=None,
        live_monitoring_enabled=False,
        scheduler_enabled=False,
        daemon_started=False,
        policy_valid=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_split_based_window_policy(reference_splits: List[str], monitoring_splits: List[str]) -> MonitoringWindowPolicy:
    return build_default_monitoring_window_policy(reference_splits, monitoring_splits)

def validate_monitoring_window_policy(policy: MonitoringWindowPolicy) -> List[str]:
    return []

def monitoring_window_policy_summary(policy: MonitoringWindowPolicy) -> Dict[str, Any]:
    return {}

def monitoring_window_policy_to_text(policy: MonitoringWindowPolicy, limit: int = 300) -> str:
    return "Monitoring Window Policy Output"
