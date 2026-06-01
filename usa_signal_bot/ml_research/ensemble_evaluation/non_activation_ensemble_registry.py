from typing import Any, Dict, List
import datetime
import hashlib

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    NonActivationEnsembleRegistry,
    NonActivationEnsembleRegistryEntry,
    create_non_activation_ensemble_registry_id,
    create_non_activation_ensemble_registry_entry_id,
    EnsemblePrototypeSpec,
    OfflineEnsemblePredictionArtifact,
    OfflineEnsembleEvaluationReport,
    EnsembleModelCardUpdate,
    NonActivationEnsembleRegistryStatus,
    EnsembleRegistryEntryStatus
)

def build_non_activation_ensemble_registry(
    specs: List[EnsemblePrototypeSpec],
    predictions: List[OfflineEnsemblePredictionArtifact],
    reports: List[OfflineEnsembleEvaluationReport],
    model_card_updates: List[EnsembleModelCardUpdate] | None = None
) -> NonActivationEnsembleRegistry:

    entries = []

    pred_map = {p.prototype_id: p for p in predictions}
    rep_map = {r.prototype_id: r for r in reports}
    mcu_map = {m.prototype_id: m for m in (model_card_updates or [])}

    for spec in specs:
        entries.append(build_non_activation_ensemble_registry_entry(
            spec,
            pred_map.get(spec.prototype_id),
            rep_map.get(spec.prototype_id),
            mcu_map.get(spec.prototype_id)
        ))

    registry = NonActivationEnsembleRegistry(
        registry_id=create_non_activation_ensemble_registry_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        registry_status=NonActivationEnsembleRegistryStatus.CREATED,
        registry_version="phase143.v1",
        entries=entries,
        entry_count=len(entries),
        valid_entry_count=len([e for e in entries if e.registry_status == EnsembleRegistryEntryStatus.REGISTERED]),
        blocked_entry_count=len([e for e in entries if e.registry_status == EnsembleRegistryEntryStatus.BLOCKED]),
        registry_hash=None,
        registry_valid=True,
        offline_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        broker_allowed=False,
        paper_mutation_allowed=False,
        live_inference_enabled=False,
        online_inference_enabled=False,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    registry.registry_hash = compute_non_activation_ensemble_registry_hash(registry)
    return registry

def build_non_activation_ensemble_registry_entry(
    spec: EnsemblePrototypeSpec,
    prediction: OfflineEnsemblePredictionArtifact | None = None,
    report: OfflineEnsembleEvaluationReport | None = None,
    model_card_update: EnsembleModelCardUpdate | None = None
) -> NonActivationEnsembleRegistryEntry:

    return NonActivationEnsembleRegistryEntry(
        entry_id=create_non_activation_ensemble_registry_entry_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        prototype_id=spec.prototype_id,
        candidate_group_id=spec.candidate_group_id,
        blend_plan_id=spec.blend_plan_id,
        prototype_name=spec.prototype_name,
        prototype_kind=spec.prototype_kind,
        registry_status=EnsembleRegistryEntryStatus.REGISTERED,
        prediction_artifact_id=prediction.prediction_id if prediction else None,
        evaluation_report_id=report.report_id if report else None,
        model_card_update_id=model_card_update.update_id if model_card_update else None,
        eligible_for_phase144_drift_baseline=True,
        eligible_for_live_use=False,
        eligible_for_paper_use=False,
        eligible_for_broker_use=False,
        eligible_for_deployment=False,
        eligible_for_strategy_activation=False,
        offline_research_only=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def compute_non_activation_ensemble_registry_hash(registry: NonActivationEnsembleRegistry) -> str:
    s = f"{registry.registry_id}_{len(registry.entries)}"
    return hashlib.sha256(s.encode()).hexdigest()

def validate_non_activation_ensemble_registry(registry: NonActivationEnsembleRegistry) -> List[str]:
    errors = []
    if registry.eligible_for_live_use or registry.deployment_allowed:
        errors.append("Registry allows deployment/live use")
    for e in registry.entries:
        if e.eligible_for_deployment or e.eligible_for_live_use:
            errors.append("Entry allows deployment/live use")
    return errors

def non_activation_ensemble_registry_summary(registry: NonActivationEnsembleRegistry) -> Dict[str, Any]:
    return {"entry_count": registry.entry_count}

def non_activation_ensemble_registry_to_text(registry: NonActivationEnsembleRegistry, limit: int = 300) -> str:
    return str(non_activation_ensemble_registry_summary(registry))
