from typing import List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import ReadinessStage
from .dossier_models import ObserverPromotionDossier, ReadinessStagePlan, create_readiness_stage_plan_id

def build_stage_0_dossier_only_plan(dossier: ObserverPromotionDossier) -> ReadinessStagePlan:
    return ReadinessStagePlan(
        stage_plan_id=create_readiness_stage_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        stage=ReadinessStage.STAGE_0_DOSSIER_ONLY,
        title="Stage 0: Dossier Only",
        description="Initial compilation of the promotion dossier without execution.",
        required_inputs=["observer_governance_review"],
        required_gates=["evidence_completeness"],
        output_artifacts=["ObserverPromotionDossier"],
        execution_enabled=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        warnings=[],
        errors=[]
    )

def build_stage_1_non_executing_readiness_rehearsal_plan(dossier: ObserverPromotionDossier) -> ReadinessStagePlan:
    return ReadinessStagePlan(
        stage_plan_id=create_readiness_stage_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        stage=ReadinessStage.STAGE_1_NON_EXECUTING_READINESS_REHEARSAL,
        title="Stage 1: Non-Executing Rehearsal",
        description="Dry-run simulation of the staging process.",
        required_inputs=["ObserverPromotionDossier"],
        required_gates=["non_execution_compliance"],
        output_artifacts=["RehearsalReport"],
        execution_enabled=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        warnings=[],
        errors=[]
    )

def build_stage_2_guarded_handoff_review_plan(dossier: ObserverPromotionDossier) -> ReadinessStagePlan:
    return ReadinessStagePlan(
        stage_plan_id=create_readiness_stage_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        stage=ReadinessStage.STAGE_2_GUARDED_HANDOFF_REVIEW,
        title="Stage 2: Guarded Handoff Review",
        description="Review of the rehearsal report by safety board.",
        required_inputs=["RehearsalReport"],
        required_gates=["manual_review_required"],
        output_artifacts=["HandoffReview"],
        execution_enabled=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        warnings=[],
        errors=[]
    )

def build_stage_3_final_locked_review_plan(dossier: ObserverPromotionDossier) -> ReadinessStagePlan:
    return ReadinessStagePlan(
        stage_plan_id=create_readiness_stage_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        stage=ReadinessStage.STAGE_3_FINAL_LOCKED_REVIEW,
        title="Stage 3: Final Locked Review",
        description="Final metadata review before any future phase integration.",
        required_inputs=["HandoffReview"],
        required_gates=["no_active_paper_permission"],
        output_artifacts=["FinalLockedReview"],
        execution_enabled=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        warnings=[],
        errors=[]
    )

def default_readiness_stage_plans(dossier: ObserverPromotionDossier) -> List[ReadinessStagePlan]:
    return [
        build_stage_0_dossier_only_plan(dossier),
        build_stage_1_non_executing_readiness_rehearsal_plan(dossier),
        build_stage_2_guarded_handoff_review_plan(dossier),
        build_stage_3_final_locked_review_plan(dossier)
    ]

def validate_readiness_stage_plan_safety(plan: ReadinessStagePlan) -> List[str]:
    warnings = []
    if plan.execution_enabled: warnings.append(f"{plan.stage.value} illegally enables execution.")
    if plan.active_paper_enabled: warnings.append(f"{plan.stage.value} illegally enables active paper.")
    if plan.broker_execution_enabled: warnings.append(f"{plan.stage.value} illegally enables broker execution.")
    if plan.paper_state_mutation_enabled: warnings.append(f"{plan.stage.value} illegally enables paper state mutation.")
    if plan.config_patch_enabled: warnings.append(f"{plan.stage.value} illegally enables config patch.")
    return warnings

def readiness_stage_plans_to_text(plans: List[ReadinessStagePlan], limit: int = 100) -> str:
    lines = []
    for p in plans[:limit]:
        lines.append(f"{p.stage.value}: {p.title}")
    return "\n".join(lines)
