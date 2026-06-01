import hashlib
import json
from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import EvaluationHarnessKind, BaselineMLScaffoldingQuality
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    EvaluationHarnessContract,
    EvaluationMetricSpec,
    create_evaluation_harness_contract_id,
    _now_utc
)
from usa_signal_bot.ml_research.experiment_scaffolding.prediction_output_boundary import allowed_prediction_output_kinds, forbidden_prediction_output_fields

def build_evaluation_harness_contract(dataset_manifest_payload: Optional[Dict[str, Any]], split_assignment_payload: Optional[Dict[str, Any]], metric_specs: List[EvaluationMetricSpec]) -> EvaluationHarnessContract:
    c = EvaluationHarnessContract(
        harness_id=create_evaluation_harness_contract_id(),
        created_at_utc=_now_utc(),
        harness_kind=EvaluationHarnessKind.OFFLINE_RESEARCH_EVALUATION,
        harness_version="phase138.v1",
        dataset_manifest_id=dataset_manifest_payload.get("manifest_id") if dataset_manifest_payload else None,
        split_assignment_id=split_assignment_payload.get("assignment_id") if split_assignment_payload else None,
        required_metric_specs=metric_specs,
        accepted_prediction_boundary_kinds=allowed_prediction_output_kinds(),
        allowed_input_artifacts=["dataset_manifest", "split_assignment", "feature_matrix", "target_matrix", "label_matrix"],
        forbidden_output_fields=forbidden_prediction_output_fields(),
        training_allowed_in_phase138=False,
        prediction_allowed_in_phase138=False,
        live_evaluation_allowed=False,
        broker_evaluation_allowed=False,
        paper_mutation_allowed=False,
        contract_hash=None,
        contract_valid=False,
        quality=BaselineMLScaffoldingQuality.HIGH,
        research_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )
    c.contract_valid = len(validate_evaluation_harness_contract(c)) == 0
    if c.contract_valid:
        c.contract_hash = compute_evaluation_harness_contract_hash(c)
    return c

def default_forbidden_evaluation_output_fields() -> List[str]:
    return forbidden_prediction_output_fields()

def compute_evaluation_harness_contract_hash(contract: EvaluationHarnessContract) -> str:
    s = f"{contract.harness_id}_{contract.harness_version}_{contract.training_allowed_in_phase138}_{contract.prediction_allowed_in_phase138}"
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def validate_evaluation_harness_contract(contract: EvaluationHarnessContract) -> List[str]:
    errors = []
    if contract.training_allowed_in_phase138:
        errors.append("training_allowed_in_phase138 is true")
    if contract.prediction_allowed_in_phase138:
        errors.append("prediction_allowed_in_phase138 is true")
    if contract.live_evaluation_allowed:
        errors.append("live_evaluation_allowed is true")
    if contract.broker_evaluation_allowed:
        errors.append("broker_evaluation_allowed is true")
    if contract.paper_mutation_allowed:
        errors.append("paper_mutation_allowed is true")
    if contract.produces_trade_signal or contract.produces_order_decision or contract.produces_portfolio_weights:
        errors.append("Harness produces trade signal or order semantics")
    return errors

def evaluation_harness_contract_summary(contract: EvaluationHarnessContract) -> Dict[str, Any]:
    return {
        "valid": contract.contract_valid,
        "hash": contract.contract_hash,
        "version": contract.harness_version,
        "metrics_count": len(contract.required_metric_specs)
    }

def evaluation_harness_contract_to_text(contract: EvaluationHarnessContract, limit: int = 300) -> str:
    summary = evaluation_harness_contract_summary(contract)
    return f"Evaluation Harness Contract: Valid={summary['valid']}, Hash={summary['hash']}, Metrics={summary['metrics_count']}"
