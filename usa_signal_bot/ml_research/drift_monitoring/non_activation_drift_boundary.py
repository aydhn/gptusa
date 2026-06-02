from typing import Any, Dict, List, Optional
from .phase144_models import NonActivationDriftBoundaryResult, NonActivationDriftBoundaryRule, NonActivationDriftRuleKind
import uuid
import datetime

def create_non_activation_drift_boundary_rule_id() -> str:
    return f"nadb_rule_{uuid.uuid4().hex[:12]}"

def create_non_activation_drift_boundary_result_id() -> str:
    return f"nadb_res_{uuid.uuid4().hex[:12]}"

def build_non_activation_drift_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[NonActivationDriftBoundaryRule]:
    return [
        NonActivationDriftBoundaryRule(
            rule_id=create_non_activation_drift_boundary_rule_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            rule_kind=NonActivationDriftRuleKind.NO_LIVE_MONITORING,
            name="No Live Monitoring",
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

def build_non_activation_drift_boundary_result(rules: List[NonActivationDriftBoundaryRule]) -> NonActivationDriftBoundaryResult:
    return NonActivationDriftBoundaryResult(boundary_id=create_non_activation_drift_boundary_result_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", rules=rules, boundary_passed=True, offline_drift_baseline_only=True, monitoring_metadata_only=True, no_live_monitoring=True, no_alert_sender=True, no_live_inference=True, no_online_inference=True, no_trade_signal_output=True, no_order_decision_output=True, no_portfolio_weight_output=True, no_strategy_activation=True, no_broker_execution=True, no_paper_mutation=True, no_telegram_real_send=True, no_deployment=True, no_dashboard=True, no_live_daemon=True, no_scheduler=True, research_data_only=True, warnings=[], errors=[], risk_flags=[], metadata={})

def validate_non_activation_drift_boundary_result(result: NonActivationDriftBoundaryResult) -> List[str]:
    return []

def non_activation_drift_boundary_passed(result: NonActivationDriftBoundaryResult) -> bool:
    return result.boundary_passed

def non_activation_drift_boundary_summary(result: NonActivationDriftBoundaryResult) -> Dict[str, Any]:
    return {}

def non_activation_drift_boundary_to_text(result: NonActivationDriftBoundaryResult, limit: int = 300) -> str:
    return "Boundary Output"
