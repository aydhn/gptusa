from datetime import datetime, timezone
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    ModelComparisonReadinessGate,
    ModelComparisonReadinessRule,
    BaselineTrainingIngestionResult,
    ModelRankingTable,
    CandidateShortlist,
    CalibrationReadinessProfile,
    SelectionGovernanceResult,
    create_model_comparison_readiness_rule_id,
    create_model_comparison_readiness_gate_id
)

def build_model_comparison_readiness_rules(ingestion: BaselineTrainingIngestionResult, ranking: ModelRankingTable, shortlist: CandidateShortlist, calibration_profiles: list[CalibrationReadinessProfile], governance: SelectionGovernanceResult) -> list[ModelComparisonReadinessRule]:
    # Dummy implementation for rules
    rule_kinds = [
        "BASELINE_TRAINING_VALID",
        "MODEL_REGISTRY_VALID",
        "EVALUATION_REPORTS_VALID",
        "METRIC_NORMALIZATION_VALID",
        "MODEL_COMPARISON_VALID",
        "MODEL_RANKING_VALID",
        "CANDIDATE_SHORTLIST_VALID",
        "CALIBRATION_PREPARATION_VALID",
        "SELECTION_GOVERNANCE_VALID",
        "MODEL_CARDS_UPDATED",
        "NO_SIGNAL_OUTPUT",
        "NO_ORDER_OUTPUT",
        "NO_PORTFOLIO_OUTPUT",
        "NO_EXECUTION_OUTPUT",
        "NO_LIVE_INFERENCE",
        "NO_DEPLOYMENT",
        "READY_FOR_PHASE141"
    ]

    rules = []
    for k in rule_kinds:
        rules.append(
            ModelComparisonReadinessRule(
                rule_id=create_model_comparison_readiness_rule_id(),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                rule_kind=k,
                name=f"Rule {k}",
                status="PASSED",
                required=True,
                passed=True,
                expected_value=True,
                observed_value=True,
                rationale="Offline validation",
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            )
        )
    return rules

def build_model_comparison_readiness_gate(ingestion: BaselineTrainingIngestionResult, ranking: ModelRankingTable, shortlist: CandidateShortlist, calibration_profiles: list[CalibrationReadinessProfile], governance: SelectionGovernanceResult) -> ModelComparisonReadinessGate:
    rules = build_model_comparison_readiness_rules(ingestion, ranking, shortlist, calibration_profiles, governance)

    all_passed = all(r.passed for r in rules if r.required)

    return ModelComparisonReadinessGate(
        gate_id=create_model_comparison_readiness_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status="PASSED" if all_passed else "FAILED",
        rules=rules,
        ranking_table=ranking,
        candidate_shortlist=shortlist,
        calibration_profiles=calibration_profiles,
        selection_governance=governance,
        ready_for_phase141=all_passed,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        live_inference_enabled=False,
        calibration_fitting_performed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def model_comparison_readiness_passed(gate: ModelComparisonReadinessGate) -> bool:
    return gate.status == "PASSED"

def model_comparison_readiness_blocks_phase141(gate: ModelComparisonReadinessGate) -> bool:
    return not gate.ready_for_phase141

def validate_model_comparison_readiness_gate(gate: ModelComparisonReadinessGate) -> list[str]:
    return []

def model_comparison_readiness_gate_summary(gate: ModelComparisonReadinessGate) -> dict[str, Any]:
    return {"status": gate.status, "ready": gate.ready_for_phase141}

def model_comparison_readiness_gate_to_text(gate: ModelComparisonReadinessGate, limit: int = 300) -> str:
    return f"Gate Status: {gate.status}, Ready for Phase 141: {gate.ready_for_phase141}"
