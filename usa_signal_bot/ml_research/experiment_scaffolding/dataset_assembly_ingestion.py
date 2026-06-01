import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    MLDatasetAssemblyIngestionResult,
    create_ml_dataset_assembly_ingestion_id,
    _now_utc
)
from usa_signal_bot.core.enums import BaselineMLScaffoldingRiskFlag

def extract_dataset_assembly_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
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

def extract_dataset_assembly_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")

def dataset_assembly_supports_phase138(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    if not payload:
        return False, ["Payload is empty or None."]
    if not payload.get("ready_for_phase138"):
        warnings.append("Payload indicates not ready_for_phase138")
        return False, warnings
    return True, []

def ingest_dataset_assembly_review_payload(payload: Dict[str, Any]) -> MLDatasetAssemblyIngestionResult:
    warnings = []
    errors = []
    risk_flags = []

    if not payload:
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
            warnings=warnings,
            errors=errors
        )

    ctx = extract_dataset_assembly_context(payload) or {}
    ingestion = ctx.get("ingestion", {}) or {}
    manifest = extract_dataset_manifest(payload)
    splits = extract_split_assignment(payload)
    leakage = extract_leakage_audit(payload)
    readiness = extract_dataset_assembly_readiness_gate(payload)

    ready_for_phase138 = payload.get("ready_for_phase138", False)
    if not ready_for_phase138:
        risk_flags.append(BaselineMLScaffoldingRiskFlag.PHASE137_NOT_READY)

    valid_for_phase138 = True

    ml_foundation_ingested = ctx.get("ml_foundation_ingested", False)
    if not ml_foundation_ingested:
        valid_for_phase138 = False
        errors.append("ml_foundation_ingested is False")

    sources_resolved = ctx.get("sources_resolved", False)
    if not sources_resolved:
        valid_for_phase138 = False
        errors.append("sources_resolved is False")

    feature_matrix_assembled = ctx.get("feature_matrix_assembled", False)
    if not feature_matrix_assembled:
        valid_for_phase138 = False
        errors.append("feature_matrix_assembled is False")

    target_matrix_assembled = ctx.get("target_matrix_assembled", False)
    if not target_matrix_assembled:
        valid_for_phase138 = False
        errors.append("target_matrix_assembled is False")

    label_matrix_assembled = ctx.get("label_matrix_assembled", False)
    if not label_matrix_assembled:
        valid_for_phase138 = False
        errors.append("label_matrix_assembled is False")

    dataset_manifest_built = ctx.get("dataset_manifest_built", False)
    if not dataset_manifest_built:
        valid_for_phase138 = False
        errors.append("dataset_manifest_built is False")

    split_policy_built = ctx.get("split_policy_built", False)
    if not split_policy_built:
        valid_for_phase138 = False
        errors.append("split_policy_built is False")

    split_assignment_built = ctx.get("split_assignment_built", False)
    if not split_assignment_built:
        valid_for_phase138 = False
        errors.append("split_assignment_built is False")

    leakage_audit_completed = ctx.get("leakage_audit_completed", False)
    if not leakage_audit_completed:
        valid_for_phase138 = False
        errors.append("leakage_audit_completed is False")

    dataset_quality_evaluated = ctx.get("dataset_quality_evaluated", False)
    if not dataset_quality_evaluated:
        valid_for_phase138 = False
        errors.append("dataset_quality_evaluated is False")

    split_quality_evaluated = ctx.get("split_quality_evaluated", False)
    if not split_quality_evaluated:
        valid_for_phase138 = False
        errors.append("split_quality_evaluated is False")

    readiness_gate_passed = ctx.get("readiness_gate_passed", False)
    if not readiness_gate_passed:
        valid_for_phase138 = False
        errors.append("readiness_gate_passed is False")

    # Safety checks
    if not payload.get("research_data_only", True):
        valid_for_phase138 = False
        errors.append("research_data_only is False")
        risk_flags.append(BaselineMLScaffoldingRiskFlag.DATASET_ASSEMBLY_REVIEW_INVALID)

    for field_name in ["activation_allowed", "strategy_activation_allowed", "deployment_allowed", "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled", "html_parse_enabled", "paid_api_enabled", "dashboard_enabled", "network_default_enabled", "daemon_started", "scheduler_enabled", "training_started", "prediction_started", "model_training_used", "model_prediction_used", "heavy_ml_dependency_used", "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice"]:
        if payload.get(field_name, False):
            valid_for_phase138 = False
            errors.append(f"{field_name} is True")
            if "training" in field_name:
                risk_flags.append(BaselineMLScaffoldingRiskFlag.MODEL_TRAINING_ATTEMPTED)
            elif "prediction" in field_name:
                risk_flags.append(BaselineMLScaffoldingRiskFlag.MODEL_PREDICTION_ATTEMPTED)
            elif "signal" in field_name:
                risk_flags.append(BaselineMLScaffoldingRiskFlag.TRADE_SIGNAL_COLUMN_RISK)

    return MLDatasetAssemblyIngestionResult(
        ingestion_id=create_ml_dataset_assembly_ingestion_id(),
        created_at_utc=_now_utc(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=ctx.get("context_id"),
        available=True,
        ml_foundation_ingested=ml_foundation_ingested,
        foundation_artifacts_loaded=ctx.get("foundation_artifacts_loaded", False),
        sources_resolved=sources_resolved,
        feature_matrix_assembled=feature_matrix_assembled,
        target_matrix_assembled=target_matrix_assembled,
        label_matrix_assembled=label_matrix_assembled,
        dataset_manifest_built=dataset_manifest_built,
        split_policy_built=split_policy_built,
        split_assignment_built=split_assignment_built,
        leakage_audit_completed=leakage_audit_completed,
        dataset_quality_evaluated=dataset_quality_evaluated,
        split_quality_evaluated=split_quality_evaluated,
        readiness_gate_built=ctx.get("readiness_gate_built", False),
        readiness_gate_passed=readiness_gate_passed,
        ready_for_phase138=ready_for_phase138,
        metadata_only=payload.get("metadata_only", True),
        research_data_only=payload.get("research_data_only", True),
        activation_allowed=payload.get("activation_allowed", False),
        strategy_activation_allowed=payload.get("strategy_activation_allowed", False),
        deployment_allowed=payload.get("deployment_allowed", False),
        active_paper_enabled=payload.get("active_paper_enabled", False),
        broker_execution_enabled=payload.get("broker_execution_enabled", False),
        order_creation_enabled=payload.get("order_creation_enabled", False),
        paper_state_mutation_enabled=payload.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=payload.get("telegram_real_send_enabled", False),
        scraping_enabled=payload.get("scraping_enabled", False),
        html_parse_enabled=payload.get("html_parse_enabled", False),
        paid_api_enabled=payload.get("paid_api_enabled", False),
        dashboard_enabled=payload.get("dashboard_enabled", False),
        network_default_enabled=payload.get("network_default_enabled", False),
        daemon_started=payload.get("daemon_started", False),
        scheduler_enabled=payload.get("scheduler_enabled", False),
        training_started=payload.get("training_started", False),
        prediction_started=payload.get("prediction_started", False),
        model_training_used=payload.get("model_training_used", False),
        model_prediction_used=payload.get("model_prediction_used", False),
        heavy_ml_dependency_used=payload.get("heavy_ml_dependency_used", False),
        produces_trade_signal=payload.get("produces_trade_signal", False),
        produces_order_decision=payload.get("produces_order_decision", False),
        produces_portfolio_weights=payload.get("produces_portfolio_weights", False),
        investment_advice=payload.get("investment_advice", False),
        network_used=payload.get("network_used", False),
        paid_api_used=payload.get("paid_api_used", False),
        scraping_used=payload.get("scraping_used", False),
        html_parsing_used=payload.get("html_parsing_used", False),
        broker_used=payload.get("broker_used", False),
        order_created=payload.get("order_created", False),
        paper_state_mutated=payload.get("paper_state_mutated", False),
        telegram_real_sent=payload.get("telegram_real_sent", False),
        dashboard_started=payload.get("dashboard_started", False),
        valid_for_phase138=valid_for_phase138,
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors
    )

def ingest_latest_dataset_assembly_review_from_store(data_root: Path) -> MLDatasetAssemblyIngestionResult:
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
        f"Readiness Gate Passed: {result.readiness_gate_passed}"
    ]
    if result.errors:
        out.append(f"Errors: {', '.join(result.errors)}")
    if result.risk_flags:
        out.append(f"Risk Flags: {', '.join(rf.value for rf in result.risk_flags)}")
    return "\n".join(out)
