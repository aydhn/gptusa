import hashlib
from typing import List, Dict, Any
from usa_signal_bot.core.enums import ExperimentRegistryStatus, BaselineMLScaffoldingQuality
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    BaselineExperimentRegistry,
    BaselineExperimentSpec,
    BaselineModelFamilySpec,
    EvaluationMetricSpec,
    ModelCardDraft,
    ModelArtifactPlaceholder,
    create_baseline_experiment_registry_id,
    create_model_artifact_placeholder_id,
    _now_utc
)

def build_model_artifact_placeholders(experiment_specs: List[BaselineExperimentSpec]) -> List[ModelArtifactPlaceholder]:
    placeholders = []
    for spec in experiment_specs:
        placeholders.append(ModelArtifactPlaceholder(
            placeholder_id=create_model_artifact_placeholder_id(),
            created_at_utc=_now_utc(),
            placeholder_name=f"Artifact Placeholder for {spec.experiment_name}",
            experiment_id=spec.experiment_id,
            model_family_kind=spec.model_family.family_kind,
            artifact_path=None,
            artifact_hash=None,
            created_by_training=False,
            training_deferred_to_phase139=True,
            prediction_deferred_to_phase139=True,
            deployment_allowed=False,
            broker_allowed=False,
            strategy_activation_allowed=False,
            research_metadata_only=True
        ))
    return placeholders

def build_baseline_experiment_registry(experiment_specs: List[BaselineExperimentSpec], model_family_specs: List[BaselineModelFamilySpec], metric_specs: List[EvaluationMetricSpec], model_card_drafts: List[ModelCardDraft]) -> BaselineExperimentRegistry:
    placeholders = build_model_artifact_placeholders(experiment_specs)

    reg = BaselineExperimentRegistry(
        registry_id=create_baseline_experiment_registry_id(),
        created_at_utc=_now_utc(),
        registry_status=ExperimentRegistryStatus.CREATED,
        experiment_specs=experiment_specs,
        model_family_specs=model_family_specs,
        metric_specs=metric_specs,
        model_placeholders=placeholders,
        model_card_drafts=model_card_drafts,
        experiment_count=len(experiment_specs),
        registry_hash=None,
        registry_valid=False,
        quality=BaselineMLScaffoldingQuality.HIGH,
        research_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        training_started=False,
        prediction_started=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )
    reg.registry_valid = len(validate_baseline_experiment_registry(reg)) == 0
    if reg.registry_valid:
        reg.registry_hash = compute_baseline_experiment_registry_hash(reg)
    return reg

def compute_baseline_experiment_registry_hash(registry: BaselineExperimentRegistry) -> str:
    s = f"{registry.registry_id}_{registry.experiment_count}_{len(registry.model_family_specs)}_{len(registry.metric_specs)}_{len(registry.model_card_drafts)}"
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def validate_baseline_experiment_registry(registry: BaselineExperimentRegistry) -> List[str]:
    errors = []
    if registry.training_started or registry.prediction_started:
        errors.append("Training or prediction started is true")
    if registry.model_training_used or registry.model_prediction_used:
        errors.append("Model training/prediction used")
    if registry.activation_allowed or registry.strategy_activation_allowed or registry.deployment_allowed:
        errors.append("Activation/deployment is allowed")
    for ph in registry.model_placeholders:
        if ph.created_by_training:
            errors.append(f"Placeholder {ph.placeholder_name} created by training")
        if not ph.training_deferred_to_phase139:
            errors.append(f"Placeholder {ph.placeholder_name} training not deferred")
    return errors

def baseline_experiment_registry_summary(registry: BaselineExperimentRegistry) -> Dict[str, Any]:
    return {
        "valid": registry.registry_valid,
        "hash": registry.registry_hash,
        "experiments": registry.experiment_count
    }

def baseline_experiment_registry_to_text(registry: BaselineExperimentRegistry, limit: int = 300) -> str:
    summary = baseline_experiment_registry_summary(registry)
    return f"Experiment Registry: Valid={summary['valid']}, Hash={summary['hash']}, Count={summary['experiments']}"
