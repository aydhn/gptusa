from typing import Any, Dict, List, Optional
from .phase144_models import MonitoringMetadataPackage, MonitoringWindowPolicy, DriftBaselineSpec, MonitoringSnapshotSpec, DriftAlertRuleMetadata
import uuid
import datetime

def create_monitoring_metadata_package_id() -> str:
    return f"mon_pkg_{uuid.uuid4().hex[:12]}"

def build_monitoring_metadata_package(policy: MonitoringWindowPolicy, specs: List[DriftBaselineSpec], snapshot: MonitoringSnapshotSpec, alert_rules: List[DriftAlertRuleMetadata]) -> MonitoringMetadataPackage:
    return MonitoringMetadataPackage(package_id=create_monitoring_metadata_package_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", package_name="package", window_policy=policy, baseline_specs=specs, monitoring_snapshot=snapshot, alert_rule_metadata=alert_rules, package_hash=None, package_status=None, metadata_only=True, live_monitoring_enabled=False, alert_sender_enabled=False, telegram_real_send_enabled=False, dashboard_enabled=False, scheduler_enabled=False, daemon_started=False, research_data_only=True, offline_ml_research_only=True, warnings=[], errors=[], risk_flags=[], metadata={})

def compute_monitoring_metadata_package_hash(package: MonitoringMetadataPackage) -> str:
    return ""

def validate_monitoring_metadata_package(package: MonitoringMetadataPackage) -> List[str]:
    return []

def monitoring_metadata_package_summary(package: MonitoringMetadataPackage) -> Dict[str, Any]:
    return {}

def monitoring_metadata_package_to_text(package: MonitoringMetadataPackage, limit: int = 300) -> str:
    return "Package"
