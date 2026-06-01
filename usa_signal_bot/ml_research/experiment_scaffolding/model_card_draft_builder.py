import hashlib
from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import ModelCardSectionKind
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    ModelCardDraft,
    ModelCardDraftSection,
    BaselineExperimentSpec,
    EvaluationHarnessContract,
    PredictionOutputBoundary,
    create_model_card_draft_id,
    create_model_card_draft_section_id,
    _now_utc
)

def build_default_model_card_sections(experiment: BaselineExperimentSpec, harness: EvaluationHarnessContract, boundary: PredictionOutputBoundary) -> List[ModelCardDraftSection]:
    sections = []
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.MODEL_PURPOSE,
        title="Model Purpose",
        body="This model serves as a baseline research placeholder. It is not intended for live deployment or execution.",
        bullet_points=["Research only", "Non-activation"]
    ))
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.DATASET_SCOPE,
        title="Dataset Scope",
        body="Defines the static dataset boundary based on Phase 137 assembly.",
        bullet_points=[]
    ))
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.FEATURE_TARGET_LABEL_SCOPE,
        title="Feature & Target Scope",
        body="Outlines the expected input features and prediction targets.",
        bullet_points=[]
    ))
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.TRAINING_STATUS,
        title="Training Status",
        body="Training deferred to Phase 139. Currently a draft.",
        bullet_points=[]
    ))
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.EVALUATION_PLAN,
        title="Evaluation Plan",
        body="Evaluation harness will compute specific metrics offline.",
        bullet_points=[]
    ))
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.LIMITATIONS,
        title="Limitations",
        body="Draft model card. Lacks actual weights and performance metrics.",
        bullet_points=[]
    ))
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.SAFETY_BOUNDARY,
        title="Safety Boundary",
        body="Predictions are strictly bounded. No execution logic permitted.",
        bullet_points=[]
    ))
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.NON_ACTIVATION_NOTICE,
        title="Non-Activation Notice",
        body="This card does not authorize broker execution or strategy activation.",
        bullet_points=[]
    ))
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.EXPECTED_ARTIFACTS,
        title="Expected Artifacts",
        body="Lists expected artifact paths for the final model.",
        bullet_points=[]
    ))
    sections.append(ModelCardDraftSection(
        section_id=create_model_card_draft_section_id(),
        created_at_utc=_now_utc(),
        section_kind=ModelCardSectionKind.GOVERNANCE,
        title="Governance",
        body="Subject to Phase 138 scaffolding governance policies.",
        bullet_points=[]
    ))
    return sections

def build_model_card_draft_for_experiment(experiment: BaselineExperimentSpec, harness: EvaluationHarnessContract, boundary: PredictionOutputBoundary) -> ModelCardDraft:
    sections = build_default_model_card_sections(experiment, harness, boundary)
    c = ModelCardDraft(
        card_id=create_model_card_draft_id(),
        created_at_utc=_now_utc(),
        card_title=f"Draft Model Card: {experiment.experiment_name}",
        card_version="0.1.0-draft",
        experiment_id=experiment.experiment_id,
        model_family_kind=experiment.model_family.family_kind,
        sections=sections,
        rendered_markdown=None,
        rendered_text=None,
        card_hash=None,
        draft_only=True,
        training_not_started=True,
        prediction_not_started=True,
        not_investment_advice=True,
        not_trade_signal=True,
        not_deployment_artifact=True,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )
    c.rendered_markdown = render_model_card_markdown(c)
    c.rendered_text = render_model_card_text(c)
    c.card_hash = compute_model_card_hash(c)
    return c

def render_model_card_markdown(card: ModelCardDraft) -> str:
    lines = [f"# {card.card_title} (Version: {card.card_version})"]
    for section in card.sections:
        lines.append(f"## {section.title}")
        lines.append(section.body)
        for bullet in section.bullet_points:
            lines.append(f"- {bullet}")
        lines.append("")
    return "\n".join(lines)

def render_model_card_text(card: ModelCardDraft) -> str:
    return render_model_card_markdown(card)

def compute_model_card_hash(card: ModelCardDraft) -> str:
    s = f"{card.card_title}_{card.experiment_id}_{len(card.sections)}_{card.training_not_started}"
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def validate_model_card_draft(card: ModelCardDraft) -> List[str]:
    errors = []
    if not card.draft_only:
        errors.append("draft_only is false")
    if not card.training_not_started:
        errors.append("training_not_started is false")
    if not card.prediction_not_started:
        errors.append("prediction_not_started is false")
    if not card.not_investment_advice:
        errors.append("not_investment_advice is false")
    if not card.not_trade_signal:
        errors.append("not_trade_signal is false")
    if not card.not_deployment_artifact:
        errors.append("not_deployment_artifact is false")

    text = card.rendered_text.lower() if card.rendered_text else ""
    for unsafe in ["profit", "guarantee", "buy/sell", "entry/exit", "order"]:
        if unsafe in text:
            errors.append(f"Unsafe language '{unsafe}' found in model card")

    return errors

def model_card_draft_summary(card: ModelCardDraft) -> Dict[str, Any]:
    return {
        "valid": len(validate_model_card_draft(card)) == 0,
        "title": card.card_title,
        "hash": card.card_hash
    }

def model_card_draft_to_text(card: ModelCardDraft, limit: int = 300) -> str:
    summary = model_card_draft_summary(card)
    return f"Model Card Draft: {summary['title']}, Valid={summary['valid']}"
