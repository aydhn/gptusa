import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import StageRehearsalStatus
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    StageRehearsalPlan, create_stage_rehearsal_plan_id, validate_stage_rehearsal_plan
)
from usa_signal_bot.paper_readiness_rehearsal.promotion_dossier_ingestion import extract_readiness_package

def build_stage_rehearsal_plans_from_package(package_payload: Dict[str, Any]) -> List[StageRehearsalPlan]:
    pkg = extract_readiness_package(package_payload)
    if not pkg:
        return build_default_stage_rehearsal_plans()

    stages = pkg.get("stages", [])
    if not stages:
        return build_default_stage_rehearsal_plans()

    return [build_stage_rehearsal_plan(s) for s in stages]

def build_stage_rehearsal_plan(stage_payload: Dict[str, Any]) -> StageRehearsalPlan:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    plan = StageRehearsalPlan(
        stage_plan_id=create_stage_rehearsal_plan_id(),
        created_at_utc=now_utc,
        source_stage=stage_payload.get("stage_name", "UNKNOWN"),
        stage_title=stage_payload.get("stage_title", "Untitled Stage"),
        status=StageRehearsalStatus.READY,
        required_inputs=stage_payload.get("required_inputs", []),
        expected_outputs=stage_payload.get("expected_outputs", []),
        execution_enabled=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        warnings=[],
        errors=[],
        metadata=stage_payload.get("metadata", {})
    )
    validate_stage_rehearsal_plan(plan)
    return plan

def build_default_stage_rehearsal_plans() -> List[StageRehearsalPlan]:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return [
        StageRehearsalPlan(
            stage_plan_id=create_stage_rehearsal_plan_id(),
            created_at_utc=now_utc,
            source_stage="STAGE_1_NON_EXECUTING_READINESS_REHEARSAL",
            stage_title="Default Stage Rehearsal",
            status=StageRehearsalStatus.READY,
            required_inputs=[],
            expected_outputs=[],
            execution_enabled=False,
            active_paper_enabled=False,
            broker_execution_enabled=False,
            paper_state_mutation_enabled=False,
            config_patch_enabled=False,
            warnings=[],
            errors=[]
        )
    ]

def validate_stage_rehearsal_plans_safe(plans: List[StageRehearsalPlan]) -> List[str]:
    errors = []
    for p in plans:
        try:
            validate_stage_rehearsal_plan(p)
        except Exception as e:
            errors.append(str(e))
    return errors

def stage_rehearsal_plans_summary(plans: List[StageRehearsalPlan]) -> Dict[str, Any]:
    return {"plan_count": len(plans)}

def stage_rehearsal_plans_to_text(plans: List[StageRehearsalPlan], limit: int = 100) -> str:
    lines = [f"Stage Rehearsal Plans ({len(plans)} total):"]
    for p in plans[:limit]:
        lines.append(f" - {p.stage_title} [{p.source_stage}]: {p.status.value}")
    return "\n".join(lines)
