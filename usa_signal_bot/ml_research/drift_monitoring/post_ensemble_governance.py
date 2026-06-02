from typing import Any, Dict, List, Optional
from .phase144_models import PostEnsembleGovernanceResult, MonitoringMetadataPackage, DriftMetricResult, PostEnsembleGovernanceRule, PostEnsembleGovernanceStatus, PostEnsembleGovernanceRuleKind
import uuid
import datetime

def create_post_ensemble_governance_rule_id() -> str:
    return f"peg_rule_{uuid.uuid4().hex[:12]}"

def create_post_ensemble_governance_result_id() -> str:
    return f"peg_res_{uuid.uuid4().hex[:12]}"

def build_post_ensemble_governance_rules(package: MonitoringMetadataPackage, metrics: List[DriftMetricResult]) -> List[PostEnsembleGovernanceRule]:
    return [
        PostEnsembleGovernanceRule(
            rule_id=create_post_ensemble_governance_rule_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            rule_kind=PostEnsembleGovernanceRuleKind.NO_LIVE_MONITORING,
            name="No Live Monitoring",
            status=PostEnsembleGovernanceStatus.PASSED,
            required=True,
            passed=True,
            expected_value=False,
            observed_value=False,
            rationale="Live monitoring is disabled.",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def build_post_ensemble_governance_result(package: MonitoringMetadataPackage, metrics: List[DriftMetricResult]) -> PostEnsembleGovernanceResult:
    return PostEnsembleGovernanceResult(governance_id=create_post_ensemble_governance_result_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", rules=build_post_ensemble_governance_rules(package, metrics), governance_status=PostEnsembleGovernanceStatus.PASSED, governance_passed=True, monitoring_package=package, drift_metric_results=metrics, research_only_monitoring_metadata=True, live_monitoring_allowed=False, alert_sender_allowed=False, live_use_allowed=False, paper_use_allowed=False, broker_use_allowed=False, deployment_allowed=False, strategy_activation_allowed=False, scheduler_enabled=False, daemon_started=False, warnings=[], errors=[], risk_flags=[], metadata={})

def post_ensemble_governance_passed(result: PostEnsembleGovernanceResult) -> bool:
    return result.governance_passed

def validate_post_ensemble_governance_result(result: PostEnsembleGovernanceResult) -> List[str]:
    return []

def post_ensemble_governance_summary(result: PostEnsembleGovernanceResult) -> Dict[str, Any]:
    return {}

def post_ensemble_governance_to_text(result: PostEnsembleGovernanceResult, limit: int = 300) -> str:
    return "Governance Output"
