from typing import Any, Dict, List
from usa_signal_bot.core.enums import ReadinessRehearsalRiskFlag
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    StageRehearsalPlan, StageRehearsalResult
)

def collect_stage_plan_safety_flags(plan: StageRehearsalPlan) -> List[ReadinessRehearsalRiskFlag]:
    flags = []
    if plan.execution_enabled or plan.active_paper_enabled or plan.broker_execution_enabled \
       or plan.paper_state_mutation_enabled or plan.config_patch_enabled:
        flags.append(ReadinessRehearsalRiskFlag.STAGE_EXECUTION_FLAG_RISK)
    return flags

def collect_stage_result_safety_flags(result: StageRehearsalResult) -> List[ReadinessRehearsalRiskFlag]:
    flags = []
    if result.execution_attempted or result.active_paper_attempted or result.broker_execution_attempted \
       or result.paper_state_mutation_attempted or result.config_patch_attempted:
        flags.append(ReadinessRehearsalRiskFlag.STAGE_EXECUTION_FLAG_RISK)
    return flags

def validate_stage_plan_safety(plan: StageRehearsalPlan) -> List[str]:
    errors = []
    flags = collect_stage_plan_safety_flags(plan)
    if flags:
        errors.append("Stage plan contains unsafe execution flags")
    return errors

def validate_stage_result_safety(result: StageRehearsalResult) -> List[str]:
    errors = []
    flags = collect_stage_result_safety_flags(result)
    if flags:
        errors.append("Stage result contains unsafe execution attempts")
    return errors

def stage_has_blocking_flags(flags: List[ReadinessRehearsalRiskFlag]) -> bool:
    return len(flags) > 0

def stage_safety_summary(flags: List[ReadinessRehearsalRiskFlag]) -> Dict[str, Any]:
    return {"flag_count": len(flags), "blocked": stage_has_blocking_flags(flags)}

def stage_safety_validator_to_text(payload: Dict[str, Any]) -> str:
    return f"Stage Safety: {payload.get('flag_count', 0)} flags. Blocked: {payload.get('blocked', False)}"
