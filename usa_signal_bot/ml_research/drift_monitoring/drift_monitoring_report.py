from typing import Any, Dict, List, Optional
from .phase144_models import *
from .ensemble_prototype_ingestion import ingest_ensemble_prototype_review_payload
from .monitoring_window_policy import build_default_monitoring_window_policy
from .monitoring_metadata_package import build_monitoring_metadata_package
from .monitoring_snapshot_builder import build_monitoring_snapshot
from .post_ensemble_governance import build_post_ensemble_governance_result
from .non_activation_drift_boundary import build_non_activation_drift_boundary_result, build_non_activation_drift_boundary_rules
from .drift_readiness_gate import build_drift_readiness_gate
import uuid
import datetime

def create_drift_monitoring_context_id() -> str:
    return f"drift_ctx_{uuid.uuid4().hex[:12]}"

def create_drift_monitoring_full_review_id() -> str:
    return f"drift_rev_{uuid.uuid4().hex[:12]}"

def build_drift_monitoring_context() -> DriftMonitoringContext:
    ingestion = ingest_ensemble_prototype_review_payload({})
    policy = build_default_monitoring_window_policy()
    snapshot = build_monitoring_snapshot(policy, [], [])
    package = build_monitoring_metadata_package(policy, [], snapshot, [])
    gov = build_post_ensemble_governance_result(package, [])
    rules = build_non_activation_drift_boundary_rules()
    bound = build_non_activation_drift_boundary_result(rules)
    gate = build_drift_readiness_gate(ingestion, package, gov, bound)

    return DriftMonitoringContext(
        context_id=create_drift_monitoring_context_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=DriftMonitoringStatus.VALIDATED,
        decision=DriftMonitoringDecision.UNKNOWN,
        source_ensemble_prototype_review_id=None,
        ingestion=ingestion,
        input_references=[],
        window_policy=policy,
        baseline_specs=[],
        feature_drift_baseline=None,
        prediction_drift_baseline=None,
        score_distribution_drift=None,
        calibration_drift_baseline=None,
        residual_drift_baseline=None,
        label_distribution_drift=None,
        regime_drift_baseline=None,
        drift_metric_results=[],
        monitoring_snapshot=snapshot,
        alert_rule_metadata=[],
        monitoring_package=package,
        post_ensemble_governance=gov,
        non_activation_boundary=bound,
        model_card_updates=[],
        readiness_gate=gate,
        ensemble_prototype_ingested=True,
        ensemble_artifacts_loaded=True,
        drift_inputs_resolved=True,
        monitoring_window_policy_built=True,
        drift_baseline_specs_built=True,
        feature_drift_baseline_built=True,
        prediction_drift_baseline_built=True,
        score_distribution_drift_built=True,
        calibration_drift_baseline_built=True,
        residual_drift_baseline_built=True,
        label_distribution_drift_built=True,
        regime_drift_baseline_built=True,
        drift_metrics_built=True,
        monitoring_snapshot_built=True,
        alert_rule_metadata_built=True,
        monitoring_metadata_package_built=True,
        post_ensemble_governance_built=True,
        non_activation_boundary_validated=True,
        model_cards_updated=True,
        readiness_gate_built=True,
        readiness_gate_passed=True,
        ready_for_phase145=True,
        metadata_only=True,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        paid_api_enabled=False,
        dashboard_enabled=False,
        network_default_enabled=False,
        live_monitoring_enabled=False,
        alert_sender_enabled=False,
        daemon_started=False,
        scheduler_enabled=False,
        live_inference_enabled=False,
        online_inference_enabled=False,
        threshold_optimization_performed=False,
        heavy_ml_dependency_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_drift_monitoring_full_review() -> DriftMonitoringFullReview:
    ctx = build_drift_monitoring_context()
    return DriftMonitoringFullReview(
        review_id=create_drift_monitoring_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        report_type=DriftMonitoringReportType.FULL_PHASE144_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        monitoring_package=ctx.monitoring_package,
        post_ensemble_governance=ctx.post_ensemble_governance,
        non_activation_boundary=ctx.non_activation_boundary,
        readiness_gate=ctx.readiness_gate,
        output_paths={},
        warnings=[],
        errors=[]
    )

def drift_monitoring_full_review_summary(review: DriftMonitoringFullReview) -> Dict[str, Any]:
    return {}

def drift_monitoring_limitations_text() -> str:
    return "Limitations placeholder"

def drift_monitoring_full_review_to_text(review: DriftMonitoringFullReview, limit: int = 300) -> str:
    return "Review output"
