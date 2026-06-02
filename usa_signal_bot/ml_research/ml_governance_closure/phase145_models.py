from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.core.enums import (
    MLGovernanceClosureStatus,
    MLGovernanceClosureDecision,
    ExplainabilityInputKind,
    ExplainabilityMethodKind,
    ExplanationScope,
    ExplanationStatus,
    MLGovernanceRuleKind,
    MLGovernanceClosureRuleStatus,
    AdvancedMLAuditItemKind,
    AdvancedMLAuditStatus,
    AdvancedMLLineageNodeKind,
    AdvancedMLAcceptanceStatus,
    AdvancedMLAcceptanceRuleKind,
    NonActivationMLClosureRuleKind,
    MLClosureQuality,
    MLClosureRiskFlag,
    MLGovernanceClosureReportType
)
import uuid
import datetime
import json
import hashlib

def generate_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"

def current_time() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def create_drift_monitoring_ingestion_id() -> str:
    return generate_id("ing")

def create_explainability_input_reference_id() -> str:
    return generate_id("exp-in")

def create_feature_attribution_proxy_id() -> str:
    return generate_id("feat-attr")

def create_factor_contribution_summary_id() -> str:
    return generate_id("fact-cont")

def create_model_behavior_explanation_id() -> str:
    return generate_id("mod-behav")

def create_regime_aware_explanation_id() -> str:
    return generate_id("reg-exp")

def create_calibration_aware_explanation_id() -> str:
    return generate_id("cal-exp")

def create_ensemble_explanation_id() -> str:
    return generate_id("ens-exp")

def create_explainability_report_id() -> str:
    return generate_id("exp-rep")

def create_ml_governance_closure_rule_id() -> str:
    return generate_id("gov-rule")

def create_ml_governance_closure_result_id() -> str:
    return generate_id("gov-res")

def create_advanced_ml_lineage_node_id() -> str:
    return generate_id("lin-node")

def create_advanced_ml_artifact_lineage_id() -> str:
    return generate_id("art-lin")

def create_advanced_ml_audit_item_id() -> str:
    return generate_id("aud-item")

def create_advanced_ml_final_audit_result_id() -> str:
    return generate_id("fin-aud")

def create_non_activation_ml_closure_boundary_rule_id() -> str:
    return generate_id("na-rule")

def create_non_activation_ml_closure_boundary_result_id() -> str:
    return generate_id("na-res")

def create_final_ml_model_card_closure_id() -> str:
    return generate_id("mc-clos")

def create_advanced_ml_acceptance_rule_id() -> str:
    return generate_id("acc-rule")

def create_advanced_ml_acceptance_gate_id() -> str:
    return generate_id("acc-gate")

def create_advanced_ml_closure_context_id() -> str:
    return generate_id("clos-ctx")

def create_advanced_ml_closure_full_review_id() -> str:
    return generate_id("full-rev")

@dataclass
class DriftMonitoringIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    ensemble_prototype_ingested: bool
    ensemble_artifacts_loaded: bool
    drift_inputs_resolved: bool
    monitoring_window_policy_built: bool
    drift_baseline_specs_built: bool
    feature_drift_baseline_built: bool
    prediction_drift_baseline_built: bool
    score_distribution_drift_built: bool
    calibration_drift_baseline_built: bool
    residual_drift_baseline_built: bool
    label_distribution_drift_built: bool
    regime_drift_baseline_built: bool
    drift_metrics_built: bool
    monitoring_snapshot_built: bool
    alert_rule_metadata_built: bool
    monitoring_metadata_package_built: bool
    post_ensemble_governance_built: bool
    non_activation_boundary_validated: bool
    model_cards_updated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase145: bool
    metadata_only: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    paid_api_enabled: bool
    dashboard_enabled: bool
    network_default_enabled: bool
    live_monitoring_enabled: bool
    alert_sender_enabled: bool
    daemon_started: bool
    scheduler_enabled: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
    threshold_optimization_performed: bool
    heavy_ml_dependency_used: bool
    shap_lime_dependency_used: bool
    backtest_executed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    valid_for_phase145: bool
    risk_flags: list[MLClosureRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class ExplainabilityInputReference:
    input_ref_id: str
    created_at_utc: str
    input_kind: ExplainabilityInputKind
    source_artifact_name: str
    source_path: str | None
    source_hash: str | None
    phase_number: int | None
    model_artifact_id: str | None
    prototype_id: str | None
    registry_entry_id: str | None
    available: bool
    read_only: bool
    research_data_only: bool
    offline_ml_research_only: bool
    contains_forbidden_outputs: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureAttributionProxy:
    attribution_id: str
    created_at_utc: str
    method_kind: ExplainabilityMethodKind
    scope: ExplanationScope
    feature_name: str
    proxy_score: float | None
    rank: int | None
    direction_label: str | None
    stability_score: float | None
    drift_sensitivity_score: float | None
    attribution_notes: list[str]
    not_trade_signal: bool
    not_portfolio_weight: bool
    not_order_decision: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorContributionSummary:
    summary_id: str
    created_at_utc: str
    method_kind: ExplainabilityMethodKind
    factor_name: str
    contribution_score: float | None
    contribution_rank: int | None
    contributing_features: list[str]
    factor_group: str | None
    stability_notes: list[str]
    drift_notes: list[str]
    summary_valid: bool
    not_trade_signal: bool
    not_portfolio_weight: bool
    not_allocation: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ModelBehaviorExplanation:
    explanation_id: str
    created_at_utc: str
    model_artifact_id: str | None
    prototype_id: str | None
    scope: ExplanationScope
    behavior_summary: str
    key_drivers: list[str]
    known_limitations: list[str]
    drift_sensitivity_notes: list[str]
    calibration_notes: list[str]
    regime_notes: list[str]
    explanation_status: ExplanationStatus
    not_investment_advice: bool
    not_trade_signal: bool
    not_deployment_artifact: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class RegimeAwareExplanation:
    explanation_id: str
    created_at_utc: str
    regime_label: str | None
    prototype_id: str | None
    model_artifact_id: str | None
    regime_behavior_summary: str
    feature_driver_notes: list[str]
    factor_driver_notes: list[str]
    drift_notes: list[str]
    limitation_notes: list[str]
    explanation_status: ExplanationStatus
    not_strategy_switch: bool
    not_trade_signal: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class CalibrationAwareExplanation:
    explanation_id: str
    created_at_utc: str
    prototype_id: str | None
    model_artifact_id: str | None
    calibration_summary: str
    reliability_notes: list[str]
    brier_notes: list[str]
    ece_notes: list[str]
    limitation_notes: list[str]
    explanation_status: ExplanationStatus
    no_calibration_fitting: bool
    no_threshold_optimization: bool
    not_trade_signal: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class EnsembleExplanation:
    explanation_id: str
    created_at_utc: str
    prototype_id: str | None
    ensemble_registry_entry_id: str | None
    ensemble_summary: str
    candidate_contribution_notes: list[str]
    blend_diagnostic_notes: list[str]
    agreement_notes: list[str]
    limitation_notes: list[str]
    explanation_status: ExplanationStatus
    not_portfolio_weight: bool
    not_allocation: bool
    not_trade_signal: bool
    not_deployment_artifact: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ExplainabilityReport:
    report_id: str
    created_at_utc: str
    input_references: list[ExplainabilityInputReference]
    feature_attributions: list[FeatureAttributionProxy]
    factor_summaries: list[FactorContributionSummary]
    behavior_explanations: list[ModelBehaviorExplanation]
    regime_explanations: list[RegimeAwareExplanation]
    calibration_explanations: list[CalibrationAwareExplanation]
    ensemble_explanations: list[EnsembleExplanation]
    report_hash: str | None
    report_valid: bool
    quality: MLClosureQuality
    explainability_metadata_only: bool
    heavy_dependency_used: bool
    shap_lime_dependency_used: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    live_inference_enabled: bool
    live_monitoring_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class MLGovernanceClosureRule:
    rule_id: str
    created_at_utc: str
    rule_kind: MLGovernanceRuleKind
    name: str
    status: MLGovernanceClosureRuleStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class MLGovernanceClosureResult:
    closure_id: str
    created_at_utc: str
    rules: list[MLGovernanceClosureRule]
    closure_status: MLGovernanceClosureRuleStatus
    closure_passed: bool
    explainability_report: ExplainabilityReport
    research_only_ml_outputs: bool
    live_use_allowed: bool
    paper_use_allowed: bool
    broker_use_allowed: bool
    deployment_allowed: bool
    strategy_activation_allowed: bool
    live_monitoring_allowed: bool
    alert_sender_allowed: bool
    backtest_execution_allowed: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class AdvancedMLLineageNode:
    node_id: str
    created_at_utc: str
    node_kind: AdvancedMLLineageNodeKind
    phase_number: int
    artifact_name: str
    artifact_id: str | None
    source_path: str | None
    source_hash: str | None
    available: bool
    validated: bool
    research_data_only: bool
    non_activation: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class AdvancedMLArtifactLineage:
    lineage_id: str
    created_at_utc: str
    nodes: list[AdvancedMLLineageNode]
    phase_numbers_covered: list[int]
    missing_phase_numbers: list[int]
    lineage_hash: str | None
    lineage_complete: bool
    lineage_valid: bool
    research_data_only: bool
    non_activation: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class AdvancedMLAuditItem:
    audit_item_id: str
    created_at_utc: str
    item_kind: AdvancedMLAuditItemKind
    phase_number: int | None
    name: str
    status: AdvancedMLAuditStatus
    required: bool
    passed: bool
    summary: str
    evidence_node_ids: list[str]
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class AdvancedMLFinalAuditResult:
    audit_id: str
    created_at_utc: str
    audit_items: list[AdvancedMLAuditItem]
    total_items: int
    passed_items: int
    warning_items: int
    failed_items: int
    blocked_items: int
    audit_status: AdvancedMLAuditStatus
    audit_passed: bool
    phase136_to_145_closed: bool
    ready_for_phase146: bool
    no_activation_violations: bool
    no_execution_violations: bool
    no_deployment_violations: bool
    no_live_monitoring_violations: bool
    no_investment_advice_violations: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class NonActivationMLClosureBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: NonActivationMLClosureRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class NonActivationMLClosureBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: list[NonActivationMLClosureBoundaryRule]
    boundary_passed: bool
    offline_research_only: bool
    explainability_metadata_only: bool
    governance_closure_only: bool
    no_live_inference: bool
    no_online_inference: bool
    no_live_monitoring: bool
    no_alert_sender: bool
    no_trade_signal_output: bool
    no_order_decision_output: bool
    no_portfolio_weight_output: bool
    no_strategy_activation: bool
    no_broker_execution: bool
    no_paper_mutation: bool
    no_telegram_real_send: bool
    no_deployment: bool
    no_dashboard: bool
    no_live_daemon: bool
    no_scheduler: bool
    no_backtest_execution: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FinalMLModelCardClosure:
    closure_id: str
    created_at_utc: str
    source_model_card_update_ids: list[str]
    updated_sections: list[str]
    rendered_markdown: str | None
    rendered_text: str | None
    closure_hash: str | None
    explainability_section_closed: bool
    governance_section_closed: bool
    risk_section_closed: bool
    non_activation_notice_preserved: bool
    not_investment_advice: bool
    not_trade_signal: bool
    not_deployment_artifact: bool
    no_live_inference: bool
    no_live_monitoring: bool
    no_backtest_execution: bool
    research_data_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class AdvancedMLAcceptanceRule:
    rule_id: str
    created_at_utc: str
    rule_kind: AdvancedMLAcceptanceRuleKind
    name: str
    status: AdvancedMLAcceptanceStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class AdvancedMLAcceptanceGate:
    gate_id: str
    created_at_utc: str
    status: AdvancedMLAcceptanceStatus
    rules: list[AdvancedMLAcceptanceRule]
    explainability_report: ExplainabilityReport
    governance_closure: MLGovernanceClosureResult
    artifact_lineage: AdvancedMLArtifactLineage
    final_audit: AdvancedMLFinalAuditResult
    non_activation_boundary: NonActivationMLClosureBoundaryResult
    final_model_card_closure: FinalMLModelCardClosure
    ready_for_phase146: bool
    phase136_to_145_closed: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    live_inference_enabled: bool
    live_monitoring_enabled: bool
    backtest_executed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class AdvancedMLClosureContext:
    context_id: str
    created_at_utc: str
    status: MLGovernanceClosureStatus
    decision: MLGovernanceClosureDecision
    source_drift_monitoring_review_id: str | None
    ingestion: DriftMonitoringIngestionResult
    input_references: list[ExplainabilityInputReference]
    explainability_report: ExplainabilityReport
    artifact_lineage: AdvancedMLArtifactLineage
    governance_closure: MLGovernanceClosureResult
    final_audit: AdvancedMLFinalAuditResult
    non_activation_boundary: NonActivationMLClosureBoundaryResult
    final_model_card_closure: FinalMLModelCardClosure
    acceptance_gate: AdvancedMLAcceptanceGate
    drift_monitoring_ingested: bool
    drift_artifacts_loaded: bool
    explainability_inputs_resolved: bool
    feature_attribution_built: bool
    factor_contribution_built: bool
    model_behavior_explanation_built: bool
    regime_aware_explanation_built: bool
    calibration_aware_explanation_built: bool
    ensemble_explanation_built: bool
    explainability_report_built: bool
    artifact_lineage_built: bool
    ml_governance_closure_built: bool
    advanced_ml_final_audit_built: bool
    non_activation_boundary_validated: bool
    final_model_cards_updated: bool
    acceptance_gate_built: bool
    acceptance_gate_passed: bool
    ready_for_phase146: bool
    phase136_to_145_closed: bool
    metadata_only: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    paid_api_enabled: bool
    dashboard_enabled: bool
    network_default_enabled: bool
    live_monitoring_enabled: bool
    alert_sender_enabled: bool
    daemon_started: bool
    scheduler_enabled: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
    threshold_optimization_performed: bool
    backtest_executed: bool
    heavy_ml_dependency_used: bool
    shap_lime_dependency_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[MLClosureRiskFlag]
    metadata: dict[str, Any]

@dataclass
class AdvancedMLClosureFullReview:
    review_id: str
    created_at_utc: str
    report_type: MLGovernanceClosureReportType
    ingestion: DriftMonitoringIngestionResult
    context: AdvancedMLClosureContext
    explainability_report: ExplainabilityReport
    governance_closure: MLGovernanceClosureResult
    artifact_lineage: AdvancedMLArtifactLineage
    final_audit: AdvancedMLFinalAuditResult
    non_activation_boundary: NonActivationMLClosureBoundaryResult
    final_model_card_closure: FinalMLModelCardClosure
    acceptance_gate: AdvancedMLAcceptanceGate
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]
