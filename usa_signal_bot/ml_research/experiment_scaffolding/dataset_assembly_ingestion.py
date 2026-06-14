import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    MLDatasetAssemblyIngestionResult,
    create_ml_dataset_assembly_ingestion_id,
    _now_utc,
)
from usa_signal_bot.core.enums import BaselineMLScaffoldingRiskFlag


def extract_dataset_assembly_context(
    payload: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    return payload.get("context")


def extract_dataset_manifest(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ctx = payload.get("context", {})
    return ctx.get("manifest") if isinstance(ctx, dict) else None


def extract_split_assignment(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ctx = payload.get("context", {})
    return ctx.get("split_assignment") if isinstance(ctx, dict) else None


def extract_leakage_audit(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ctx = payload.get("context", {})
    return ctx.get("leakage_audit_result") if isinstance(ctx, dict) else None


def extract_dataset_assembly_readiness_gate(
    payload: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")


def dataset_assembly_supports_phase138(
    payload: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    warnings = []
    if not payload:
        return False, ["Payload is empty or None."]
    if not payload.get("ready_for_phase138"):
        warnings.append("Payload indicates not ready_for_phase138")
        return False, warnings
    return True, []


def _handle_empty_payload(
    errors: List[str], risk_flags: List[BaselineMLScaffoldingRiskFlag]
) -> MLDatasetAssemblyIngestionResult:
    errors.append("Empty payload.")
    risk_flags.append(BaselineMLScaffoldingRiskFlag.DATASET_ASSEMBLY_REVIEW_MISSING)
    return MLDatasetAssemblyIngestionResult(
        ingestion_id=create_ml_dataset_assembly_ingestion_id(),
        created_at_utc=_now_utc(),
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=False,
        ml_foundation_ingested=False,
        foundation_artifacts_loaded=False,
        sources_resolved=False,
        feature_matrix_assembled=False,
        target_matrix_assembled=False,
        label_matrix_assembled=False,
        dataset_manifest_built=False,
        split_policy_built=False,
        split_assignment_built=False,
        leakage_audit_completed=False,
        dataset_quality_evaluated=False,
        split_quality_evaluated=False,
        readiness_gate_built=False,
        readiness_gate_passed=False,
        ready_for_phase138=False,
        metadata_only=True,
        research_data_only=True,
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
        daemon_started=False,
        scheduler_enabled=False,
        training_started=False,
        prediction_started=False,
        model_training_used=False,
        model_prediction_used=False,
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
        valid_for_phase138=False,
        risk_flags=risk_flags,
        warnings=[],
        errors=errors,
    )


def _check_context_flags(
    ctx: Dict[str, Any], errors: List[str]
) -> Tuple[bool, Dict[str, bool]]:
    valid_for_phase138 = True
    flags = {}
    context_keys = [
        "ml_foundation_ingested",
        "sources_resolved",
        "feature_matrix_assembled",
        "target_matrix_assembled",
        "label_matrix_assembled",
        "dataset_manifest_built",
        "split_policy_built",
        "split_assignment_built",
        "leakage_audit_completed",
        "dataset_quality_evaluated",
        "split_quality_evaluated",
        "readiness_gate_passed",
    ]
    for key in context_keys:
        val = ctx.get(key, False)
        flags[key] = val
        if not val:
            valid_for_phase138 = False
            errors.append(f"{key} is False")
    return valid_for_phase138, flags


def _perform_safety_checks(
    payload: Dict[str, Any],
    errors: List[str],
    risk_flags: List[BaselineMLScaffoldingRiskFlag],
) -> Tuple[bool, Dict[str, bool]]:
    valid_for_phase138 = True
    flags = {}

    research_data_only = payload.get("research_data_only", True)
    flags["research_data_only"] = research_data_only
    if not research_data_only:
        valid_for_phase138 = False
        errors.append("research_data_only is False")
        risk_flags.append(BaselineMLScaffoldingRiskFlag.DATASET_ASSEMBLY_REVIEW_INVALID)

    safety_keys = [
        "activation_allowed",
        "strategy_activation_allowed",
        "deployment_allowed",
        "active_paper_enabled",
        "broker_execution_enabled",
        "order_creation_enabled",
        "paper_state_mutation_enabled",
        "telegram_real_send_enabled",
        "scraping_enabled",
        "html_parse_enabled",
        "paid_api_enabled",
        "dashboard_enabled",
        "network_default_enabled",
        "daemon_started",
        "scheduler_enabled",
        "training_started",
        "prediction_started",
        "model_training_used",
        "model_prediction_used",
        "heavy_ml_dependency_used",
        "produces_trade_signal",
        "produces_order_decision",
        "produces_portfolio_weights",
        "investment_advice",
    ]
    for field_name in safety_keys:
        val = payload.get(field_name, False)
        flags[field_name] = val
        if val:
            valid_for_phase138 = False
            errors.append(f"{field_name} is True")
            if "training" in field_name:
                risk_flags.append(
                    BaselineMLScaffoldingRiskFlag.MODEL_TRAINING_ATTEMPTED
                )
            elif "prediction" in field_name:
                risk_flags.append(
                    BaselineMLScaffoldingRiskFlag.MODEL_PREDICTION_ATTEMPTED
                )
            elif "signal" in field_name:
                risk_flags.append(
                    BaselineMLScaffoldingRiskFlag.TRADE_SIGNAL_COLUMN_RISK
                )

    other_keys = [
        "network_used",
        "paid_api_used",
        "scraping_used",
        "html_parsing_used",
        "broker_used",
        "order_created",
        "paper_state_mutated",
        "telegram_real_sent",
        "dashboard_started",
    ]
    for key in other_keys:
        flags[key] = payload.get(key, False)

    return valid_for_phase138, flags


def ingest_dataset_assembly_review_payload(
    payload: Dict[str, Any],
) -> MLDatasetAssemblyIngestionResult:

    warnings = []
    errors = []
    risk_flags = []

    if not payload:
        return _handle_empty_payload(errors, risk_flags)

    ctx = extract_dataset_assembly_context(payload) or {}

    ready_for_phase138 = payload.get("ready_for_phase138", False)
    if not ready_for_phase138:
        risk_flags.append(BaselineMLScaffoldingRiskFlag.PHASE137_NOT_READY)

    valid_for_phase138_ctx, context_flags = _check_context_flags(ctx, errors)
    valid_for_phase138_safety, safety_flags = _perform_safety_checks(
        payload, errors, risk_flags
    )

    valid_for_phase138 = valid_for_phase138_ctx and valid_for_phase138_safety

    return MLDatasetAssemblyIngestionResult(
        ingestion_id=create_ml_dataset_assembly_ingestion_id(),
        created_at_utc=_now_utc(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=ctx.get("context_id"),
        available=True,
        foundation_artifacts_loaded=ctx.get("foundation_artifacts_loaded", False),
        readiness_gate_built=ctx.get("readiness_gate_built", False),
        ready_for_phase138=ready_for_phase138,
        metadata_only=payload.get("metadata_only", True),
        valid_for_phase138=valid_for_phase138,
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors,
        **context_flags,
        **safety_flags,
    )


def ingest_latest_dataset_assembly_review_from_store(
    data_root: Path,
) -> MLDatasetAssemblyIngestionResult:
    reviews_dir = data_root / "ml_research" / "dataset_assembly" / "reviews"
    if not reviews_dir.exists():
        return ingest_dataset_assembly_review_payload({})

    paths = list(reviews_dir.glob("*.json"))
    if not paths:
        return ingest_dataset_assembly_review_payload({})

    paths.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    try:
        data = json.loads(paths[0].read_text())
        res = ingest_dataset_assembly_review_payload(data)
        res.source_path = str(paths[0])
        return res
    except Exception as e:
        res = ingest_dataset_assembly_review_payload({})
        res.errors.append(f"Failed to load latest review: {e}")
        return res


def dataset_assembly_ingestion_to_text(result: MLDatasetAssemblyIngestionResult) -> str:
    out = [
        f"Ingestion ID: {result.ingestion_id}",
        f"Valid for Phase 138: {result.valid_for_phase138}",
        f"Ready for Phase 138: {result.ready_for_phase138}",
        f"ML Foundation Ingested: {result.ml_foundation_ingested}",
        f"Feature Matrix Assembled: {result.feature_matrix_assembled}",
        f"Dataset Manifest Built: {result.dataset_manifest_built}",
        f"Split Assignment Built: {result.split_assignment_built}",
        f"Leakage Audit Completed: {result.leakage_audit_completed}",
        f"Readiness Gate Passed: {result.readiness_gate_passed}",
    ]
    if result.errors:
        out.append(f"Errors: {', '.join(result.errors)}")
    if result.risk_flags:
        out.append(f"Risk Flags: {', '.join(rf.value for rf in result.risk_flags)}")
    return "\n".join(out)
