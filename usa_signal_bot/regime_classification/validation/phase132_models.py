from dataclasses import dataclass, field
from typing import Any, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    RegimeContextValidationStatus,
    RegimeContextValidationDecision,
    CompatibilityValidationRuleKind,
    CompatibilityValidationStatus,
    ConditionalDiagnosticKind,
    RegimeContextAcceptanceStatus,
    RegimeContextAcceptanceRuleKind,
    ConditionalDiagnosticSeverity,
    RegimeContextValidationQuality,
    RegimeContextValidationRiskFlag,
    RegimeContextValidationReportType
)

def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class RegimeAlignmentIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    market_behavior_ingested: bool
    frozen_factors_loaded: bool
    behavior_artifacts_loaded: bool
    alignment_specs_ready: bool
    overlays_built: bool
    compatibility_computed: bool
    diagnostics_built: bool
    readiness_gate_ready: bool
    ready_for_phase132: bool
    metadata_only: bool
    research_data_only: bool
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
    model_training_used: bool
    model_prediction_used: bool
    heavy_ml_dependency_used: bool
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
    valid_for_phase132: bool
    risk_flags: list[RegimeContextValidationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class CompatibilityValidationRule:
    rule_id: str
    created_at_utc: str
    rule_kind: CompatibilityValidationRuleKind
    name: str
    status: CompatibilityValidationStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeContextValidationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class CompatibilityValidationResult:
    validation_id: str
    created_at_utc: str
    rules: list[CompatibilityValidationRule]
    total_rules: int
    passed_rules: int
    warning_rules: int
    failed_rules: int
    blocked_rules: int
    validation_passed: bool
    compatibility_result_count: int
    overlay_result_count: int
    diagnostics_profile_count: int
    low_compatibility_count: int
    uncertain_count: int
    conflicted_count: int
    data_quality_limited_count: int
    explained_low_compatibility_count: int
    explained_uncertain_count: int
    explained_conflicted_count: int
    explained_data_quality_limited_count: int
    quality: RegimeContextValidationQuality
    research_metadata_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeContextValidationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ConditionalDiagnosticSpec:
    spec_id: str
    created_at_utc: str
    spec_name: str
    diagnostic_kind: ConditionalDiagnosticKind
    trigger_conditions: list[str]
    required_fields: list[str]
    severity: ConditionalDiagnosticSeverity
    deterministic: bool
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeContextValidationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ConditionalDiagnosticResult:
    diagnostic_id: str
    created_at_utc: str
    symbol: Optional[str]
    source_compatibility_id: Optional[str]
    diagnostic_kind: ConditionalDiagnosticKind
    severity: ConditionalDiagnosticSeverity
    condition_name: str
    condition_triggered: bool
    diagnostic_text: str
    supporting_metrics: dict[str, Any]
    recommended_action_type: str
    required_human_review: bool
    research_metadata_only: bool
    investment_advice: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeContextValidationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ConditionalDiagnosticsProfile:
    profile_id: str
    created_at_utc: str
    symbol: Optional[str]
    diagnostic_count: int
    warning_count: int
    blocking_count: int
    low_compatibility_diagnostic_count: int
    uncertain_diagnostic_count: int
    conflicted_diagnostic_count: int
    data_quality_limited_diagnostic_count: int
    profile_summary: str
    quality: RegimeContextValidationQuality
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeContextValidationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeContextAcceptanceRule:
    rule_id: str
    created_at_utc: str
    rule_kind: RegimeContextAcceptanceRuleKind
    name: str
    status: RegimeContextAcceptanceStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeContextValidationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeAwareAcceptanceGate:
    gate_id: str
    created_at_utc: str
    status: RegimeContextAcceptanceStatus
    rules: list[RegimeContextAcceptanceRule]
    compatibility_validation: CompatibilityValidationResult
    conditional_diagnostics: list[ConditionalDiagnosticResult]
    diagnostics_profiles: list[ConditionalDiagnosticsProfile]
    ready_for_phase133: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeContextValidationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeContextValidationContext:
    context_id: str
    created_at_utc: str
    status: RegimeContextValidationStatus
    decision: RegimeContextValidationDecision
    source_regime_alignment_review_id: Optional[str]
    ingestion: RegimeAlignmentIngestionResult
    validation_result: CompatibilityValidationResult
    diagnostic_specs: list[ConditionalDiagnosticSpec]
    conditional_diagnostics: list[ConditionalDiagnosticResult]
    diagnostics_profiles: list[ConditionalDiagnosticsProfile]
    acceptance_gate: RegimeAwareAcceptanceGate
    alignment_ingested: bool
    alignment_artifacts_loaded: bool
    validation_specs_ready: bool
    compatibility_validated: bool
    conditional_diagnostics_built: bool
    acceptance_gate_built: bool
    acceptance_gate_passed: bool
    ready_for_phase133: bool
    metadata_only: bool
    research_data_only: bool
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
    model_training_used: bool
    model_prediction_used: bool
    heavy_ml_dependency_used: bool
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
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeContextValidationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeContextValidationFullReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeContextValidationReportType
    ingestion: RegimeAlignmentIngestionResult
    context: RegimeContextValidationContext
    validation_result: CompatibilityValidationResult
    conditional_diagnostics: list[ConditionalDiagnosticResult]
    diagnostics_profiles: list[ConditionalDiagnosticsProfile]
    acceptance_gate: RegimeAwareAcceptanceGate
    output_paths: dict[str, str]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def create_regime_alignment_ingestion_id() -> str:
    return f"rai_{uuid.uuid4().hex[:12]}"

def create_compatibility_validation_rule_id() -> str:
    return f"cvr_{uuid.uuid4().hex[:12]}"

def create_compatibility_validation_result_id() -> str:
    return f"cvres_{uuid.uuid4().hex[:12]}"

def create_conditional_diagnostic_spec_id() -> str:
    return f"cds_{uuid.uuid4().hex[:12]}"

def create_conditional_diagnostic_result_id() -> str:
    return f"cdr_{uuid.uuid4().hex[:12]}"

def create_conditional_diagnostics_profile_id() -> str:
    return f"cdp_{uuid.uuid4().hex[:12]}"

def create_regime_context_acceptance_rule_id() -> str:
    return f"rcar_{uuid.uuid4().hex[:12]}"

def create_regime_aware_acceptance_gate_id() -> str:
    return f"raag_{uuid.uuid4().hex[:12]}"

def create_regime_context_validation_context_id() -> str:
    return f"rcvc_{uuid.uuid4().hex[:12]}"

def create_regime_context_validation_full_review_id() -> str:
    return f"rcvfr_{uuid.uuid4().hex[:12]}"

def regime_alignment_ingestion_result_to_dict(item: RegimeAlignmentIngestionResult) -> dict[str, Any]:
    return {
        "ingestion_id": item.ingestion_id,
        "created_at_utc": item.created_at_utc,
        "source_path": item.source_path,
        "source_review_id": item.source_review_id,
        "source_context_id": item.source_context_id,
        "available": item.available,
        "market_behavior_ingested": item.market_behavior_ingested,
        "frozen_factors_loaded": item.frozen_factors_loaded,
        "behavior_artifacts_loaded": item.behavior_artifacts_loaded,
        "alignment_specs_ready": item.alignment_specs_ready,
        "overlays_built": item.overlays_built,
        "compatibility_computed": item.compatibility_computed,
        "diagnostics_built": item.diagnostics_built,
        "readiness_gate_ready": item.readiness_gate_ready,
        "ready_for_phase132": item.ready_for_phase132,
        "metadata_only": item.metadata_only,
        "research_data_only": item.research_data_only,
        "activation_allowed": item.activation_allowed,
        "strategy_activation_allowed": item.strategy_activation_allowed,
        "deployment_allowed": item.deployment_allowed,
        "active_paper_enabled": item.active_paper_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "order_creation_enabled": item.order_creation_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "scraping_enabled": item.scraping_enabled,
        "html_parse_enabled": item.html_parse_enabled,
        "paid_api_enabled": item.paid_api_enabled,
        "dashboard_enabled": item.dashboard_enabled,
        "network_default_enabled": item.network_default_enabled,
        "model_training_used": item.model_training_used,
        "model_prediction_used": item.model_prediction_used,
        "heavy_ml_dependency_used": item.heavy_ml_dependency_used,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "produces_portfolio_weights": item.produces_portfolio_weights,
        "investment_advice": item.investment_advice,
        "network_used": item.network_used,
        "paid_api_used": item.paid_api_used,
        "scraping_used": item.scraping_used,
        "html_parsing_used": item.html_parsing_used,
        "broker_used": item.broker_used,
        "order_created": item.order_created,
        "paper_state_mutated": item.paper_state_mutated,
        "telegram_real_sent": item.telegram_real_sent,
        "dashboard_started": item.dashboard_started,
        "valid_for_phase132": item.valid_for_phase132,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def compatibility_validation_rule_to_dict(item: CompatibilityValidationRule) -> dict[str, Any]:
    return {
        "rule_id": item.rule_id,
        "created_at_utc": item.created_at_utc,
        "rule_kind": item.rule_kind.value,
        "name": item.name,
        "status": item.status.value,
        "required": item.required,
        "passed": item.passed,
        "expected_value": item.expected_value,
        "observed_value": item.observed_value,
        "rationale": item.rationale,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [f.value for f in item.risk_flags],
        "metadata": item.metadata,
    }

def compatibility_validation_result_to_dict(item: CompatibilityValidationResult) -> dict[str, Any]:
    return {
        "validation_id": item.validation_id,
        "created_at_utc": item.created_at_utc,
        "rules": [compatibility_validation_rule_to_dict(r) for r in item.rules],
        "total_rules": item.total_rules,
        "passed_rules": item.passed_rules,
        "warning_rules": item.warning_rules,
        "failed_rules": item.failed_rules,
        "blocked_rules": item.blocked_rules,
        "validation_passed": item.validation_passed,
        "compatibility_result_count": item.compatibility_result_count,
        "overlay_result_count": item.overlay_result_count,
        "diagnostics_profile_count": item.diagnostics_profile_count,
        "low_compatibility_count": item.low_compatibility_count,
        "uncertain_count": item.uncertain_count,
        "conflicted_count": item.conflicted_count,
        "data_quality_limited_count": item.data_quality_limited_count,
        "explained_low_compatibility_count": item.explained_low_compatibility_count,
        "explained_uncertain_count": item.explained_uncertain_count,
        "explained_conflicted_count": item.explained_conflicted_count,
        "explained_data_quality_limited_count": item.explained_data_quality_limited_count,
        "quality": item.quality.value,
        "research_metadata_only": item.research_metadata_only,
        "activation_allowed": item.activation_allowed,
        "strategy_activation_allowed": item.strategy_activation_allowed,
        "deployment_allowed": item.deployment_allowed,
        "model_training_used": item.model_training_used,
        "model_prediction_used": item.model_prediction_used,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "produces_portfolio_weights": item.produces_portfolio_weights,
        "investment_advice": item.investment_advice,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [f.value for f in item.risk_flags],
        "metadata": item.metadata,
    }

def conditional_diagnostic_spec_to_dict(item: ConditionalDiagnosticSpec) -> dict[str, Any]:
    return {
        "spec_id": item.spec_id,
        "created_at_utc": item.created_at_utc,
        "spec_name": item.spec_name,
        "diagnostic_kind": item.diagnostic_kind.value,
        "trigger_conditions": item.trigger_conditions,
        "required_fields": item.required_fields,
        "severity": item.severity.value,
        "deterministic": item.deterministic,
        "research_metadata_only": item.research_metadata_only,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "produces_portfolio_weights": item.produces_portfolio_weights,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [f.value for f in item.risk_flags],
        "metadata": item.metadata,
    }

def conditional_diagnostic_result_to_dict(item: ConditionalDiagnosticResult) -> dict[str, Any]:
    return {
        "diagnostic_id": item.diagnostic_id,
        "created_at_utc": item.created_at_utc,
        "symbol": item.symbol,
        "source_compatibility_id": item.source_compatibility_id,
        "diagnostic_kind": item.diagnostic_kind.value,
        "severity": item.severity.value,
        "condition_name": item.condition_name,
        "condition_triggered": item.condition_triggered,
        "diagnostic_text": item.diagnostic_text,
        "supporting_metrics": item.supporting_metrics,
        "recommended_action_type": item.recommended_action_type,
        "required_human_review": item.required_human_review,
        "research_metadata_only": item.research_metadata_only,
        "investment_advice": item.investment_advice,
        "activation_allowed": item.activation_allowed,
        "strategy_activation_allowed": item.strategy_activation_allowed,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "produces_portfolio_weights": item.produces_portfolio_weights,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [f.value for f in item.risk_flags],
        "metadata": item.metadata,
    }

def conditional_diagnostics_profile_to_dict(item: ConditionalDiagnosticsProfile) -> dict[str, Any]:
    return {
        "profile_id": item.profile_id,
        "created_at_utc": item.created_at_utc,
        "symbol": item.symbol,
        "diagnostic_count": item.diagnostic_count,
        "warning_count": item.warning_count,
        "blocking_count": item.blocking_count,
        "low_compatibility_diagnostic_count": item.low_compatibility_diagnostic_count,
        "uncertain_diagnostic_count": item.uncertain_diagnostic_count,
        "conflicted_diagnostic_count": item.conflicted_diagnostic_count,
        "data_quality_limited_diagnostic_count": item.data_quality_limited_diagnostic_count,
        "profile_summary": item.profile_summary,
        "quality": item.quality.value,
        "research_metadata_only": item.research_metadata_only,
        "investment_advice": item.investment_advice,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "produces_portfolio_weights": item.produces_portfolio_weights,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [f.value for f in item.risk_flags],
        "metadata": item.metadata,
    }

def regime_context_acceptance_rule_to_dict(item: RegimeContextAcceptanceRule) -> dict[str, Any]:
    return {
        "rule_id": item.rule_id,
        "created_at_utc": item.created_at_utc,
        "rule_kind": item.rule_kind.value,
        "name": item.name,
        "status": item.status.value,
        "required": item.required,
        "passed": item.passed,
        "expected_value": item.expected_value,
        "observed_value": item.observed_value,
        "rationale": item.rationale,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [f.value for f in item.risk_flags],
        "metadata": item.metadata,
    }

def regime_aware_acceptance_gate_to_dict(item: RegimeAwareAcceptanceGate) -> dict[str, Any]:
    return {
        "gate_id": item.gate_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "rules": [regime_context_acceptance_rule_to_dict(r) for r in item.rules],
        "compatibility_validation": compatibility_validation_result_to_dict(item.compatibility_validation),
        "conditional_diagnostics": [conditional_diagnostic_result_to_dict(d) for d in item.conditional_diagnostics],
        "diagnostics_profiles": [conditional_diagnostics_profile_to_dict(p) for p in item.diagnostics_profiles],
        "ready_for_phase133": item.ready_for_phase133,
        "research_data_only": item.research_data_only,
        "activation_allowed": item.activation_allowed,
        "strategy_activation_allowed": item.strategy_activation_allowed,
        "deployment_allowed": item.deployment_allowed,
        "model_training_used": item.model_training_used,
        "model_prediction_used": item.model_prediction_used,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "produces_portfolio_weights": item.produces_portfolio_weights,
        "investment_advice": item.investment_advice,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [f.value for f in item.risk_flags],
        "metadata": item.metadata,
    }

def regime_context_validation_context_to_dict(item: RegimeContextValidationContext) -> dict[str, Any]:
    return {
        "context_id": item.context_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "source_regime_alignment_review_id": item.source_regime_alignment_review_id,
        "ingestion": regime_alignment_ingestion_result_to_dict(item.ingestion),
        "validation_result": compatibility_validation_result_to_dict(item.validation_result),
        "diagnostic_specs": [conditional_diagnostic_spec_to_dict(s) for s in item.diagnostic_specs],
        "conditional_diagnostics": [conditional_diagnostic_result_to_dict(d) for d in item.conditional_diagnostics],
        "diagnostics_profiles": [conditional_diagnostics_profile_to_dict(p) for p in item.diagnostics_profiles],
        "acceptance_gate": regime_aware_acceptance_gate_to_dict(item.acceptance_gate),
        "alignment_ingested": item.alignment_ingested,
        "alignment_artifacts_loaded": item.alignment_artifacts_loaded,
        "validation_specs_ready": item.validation_specs_ready,
        "compatibility_validated": item.compatibility_validated,
        "conditional_diagnostics_built": item.conditional_diagnostics_built,
        "acceptance_gate_built": item.acceptance_gate_built,
        "acceptance_gate_passed": item.acceptance_gate_passed,
        "ready_for_phase133": item.ready_for_phase133,
        "metadata_only": item.metadata_only,
        "research_data_only": item.research_data_only,
        "activation_allowed": item.activation_allowed,
        "strategy_activation_allowed": item.strategy_activation_allowed,
        "deployment_allowed": item.deployment_allowed,
        "active_paper_enabled": item.active_paper_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "order_creation_enabled": item.order_creation_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "scraping_enabled": item.scraping_enabled,
        "html_parse_enabled": item.html_parse_enabled,
        "paid_api_enabled": item.paid_api_enabled,
        "dashboard_enabled": item.dashboard_enabled,
        "network_default_enabled": item.network_default_enabled,
        "model_training_used": item.model_training_used,
        "model_prediction_used": item.model_prediction_used,
        "heavy_ml_dependency_used": item.heavy_ml_dependency_used,
        "produces_trade_signal": item.produces_trade_signal,
        "produces_order_decision": item.produces_order_decision,
        "produces_portfolio_weights": item.produces_portfolio_weights,
        "investment_advice": item.investment_advice,
        "network_used": item.network_used,
        "paid_api_used": item.paid_api_used,
        "scraping_used": item.scraping_used,
        "html_parsing_used": item.html_parsing_used,
        "broker_used": item.broker_used,
        "order_created": item.order_created,
        "paper_state_mutated": item.paper_state_mutated,
        "telegram_real_sent": item.telegram_real_sent,
        "dashboard_started": item.dashboard_started,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [f.value for f in item.risk_flags],
        "metadata": item.metadata,
    }

def regime_context_validation_full_review_to_dict(item: RegimeContextValidationFullReview) -> dict[str, Any]:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "ingestion": regime_alignment_ingestion_result_to_dict(item.ingestion),
        "context": regime_context_validation_context_to_dict(item.context),
        "validation_result": compatibility_validation_result_to_dict(item.validation_result),
        "conditional_diagnostics": [conditional_diagnostic_result_to_dict(d) for d in item.conditional_diagnostics],
        "diagnostics_profiles": [conditional_diagnostics_profile_to_dict(p) for p in item.diagnostics_profiles],
        "acceptance_gate": regime_aware_acceptance_gate_to_dict(item.acceptance_gate),
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_regime_alignment_ingestion_result(item: RegimeAlignmentIngestionResult) -> list[str]:
    errors = []
    if not item.ready_for_phase132:
        errors.append("Ingestion not ready for Phase 132.")
    if not item.research_data_only:
        errors.append("research_data_only must be true.")
    if item.activation_allowed:
        errors.append("activation_allowed must be false.")
    if item.strategy_activation_allowed:
        errors.append("strategy_activation_allowed must be false.")
    if item.deployment_allowed:
        errors.append("deployment_allowed must be false.")
    for attr in [
        "broker_execution_enabled", "order_creation_enabled", "paper_state_mutation_enabled",
        "telegram_real_send_enabled", "scraping_enabled", "html_parse_enabled",
        "paid_api_enabled", "dashboard_enabled", "network_default_enabled"
    ]:
        if getattr(item, attr):
            errors.append(f"{attr} must be false.")
    for attr in [
        "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights",
        "investment_advice", "model_training_used", "model_prediction_used", "heavy_ml_dependency_used"
    ]:
        if getattr(item, attr):
            errors.append(f"{attr} must be false.")
    return errors

def validate_compatibility_validation_result(item: CompatibilityValidationResult) -> list[str]:
    errors = []
    if not item.research_metadata_only:
        errors.append("research_metadata_only must be true.")
    for attr in [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "model_training_used", "model_prediction_used", "produces_trade_signal",
        "produces_order_decision", "produces_portfolio_weights", "investment_advice"
    ]:
        if getattr(item, attr):
            errors.append(f"{attr} must be false.")
    return errors

def validate_conditional_diagnostic_result(item: ConditionalDiagnosticResult) -> list[str]:
    errors = []
    if not item.research_metadata_only:
        errors.append("research_metadata_only must be true.")
    for attr in [
        "activation_allowed", "strategy_activation_allowed",
        "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice"
    ]:
        if getattr(item, attr):
            errors.append(f"{attr} must be false.")

    valid_actions = ["research_review", "data_quality_review", "documentation_review", "monitor_context", "none"]
    if item.recommended_action_type not in valid_actions:
        errors.append(f"Invalid recommended_action_type: {item.recommended_action_type}")
    return errors

def validate_regime_aware_acceptance_gate(item: RegimeAwareAcceptanceGate) -> list[str]:
    errors = []
    if not item.research_data_only:
        errors.append("research_data_only must be true.")
    if item.ready_for_phase133 and item.status != RegimeContextAcceptanceStatus.ACCEPTED and item.status != RegimeContextAcceptanceStatus.WARNING_ACCEPTED:
        errors.append("ready_for_phase133 cannot be true unless status is ACCEPTED or WARNING_ACCEPTED.")
    for attr in [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "model_training_used", "model_prediction_used", "produces_trade_signal",
        "produces_order_decision", "produces_portfolio_weights", "investment_advice"
    ]:
        if getattr(item, attr):
            errors.append(f"{attr} must be false.")
    return errors

def validate_regime_context_validation_context(item: RegimeContextValidationContext) -> list[str]:
    errors = []
    if not item.research_data_only:
        errors.append("research_data_only must be true.")
    for attr in [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled",
        "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled",
        "html_parse_enabled", "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "model_training_used", "model_prediction_used", "heavy_ml_dependency_used",
        "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice"
    ]:
        if getattr(item, attr):
            errors.append(f"{attr} must be false.")
    return errors
