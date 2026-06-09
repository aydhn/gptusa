from typing import Any, Dict, List, Optional
from usa_signal_bot.release.phase159_models import (
    AdvancedDryRunStep,
    AcceptanceScenarioMatrix,
    AcceptanceScenario,
    FinalFreezeBoundaryResult,
    create_advanced_dry_run_step_id,
    generate_timestamp,
    ReleaseCandidateStatus,
    AdvancedAcceptanceRiskFlag
)

def build_advanced_dry_run_command_preview(scenario: AcceptanceScenario) -> str:
    # safe command preview logic
    return f"python -m usa_signal_bot --dry-run --local-fixture --scenario={scenario.scenario_kind.value}"

def execute_advanced_dry_run_scenario(scenario: AcceptanceScenario) -> AdvancedDryRunStep:
    # In this phase we don't actually run a subprocess, we simulate the dry-run output safely

    cmd = build_advanced_dry_run_command_preview(scenario)

    return AdvancedDryRunStep(
        step_id=create_advanced_dry_run_step_id(),
        created_at_utc=generate_timestamp(),
        scenario_id=scenario.scenario_id,
        area_kind=scenario.area_kind,
        step_name=f"Execute {scenario.name}",
        status=ReleaseCandidateStatus.PASSED,
        command_preview=cmd,
        dry_run=True,
        local_fixture_only=True,
        executed_real_side_effect=False,
        used_network=False,
        mutated_paper_state=False,
        used_broker=False,
        created_order=False,
        sent_telegram=False,
        deployed=False,
        production_patch_applied=False,
        evidence_ref=scenario.expected_evidence[0] if scenario.expected_evidence else None,
        output_summary=f"Successfully simulated safe dry-run for {scenario.name}",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={"simulated_execution": True}
    )

def execute_advanced_dry_run_scenario_matrix(
    matrix: AcceptanceScenarioMatrix,
    boundary: Optional[FinalFreezeBoundaryResult] = None
) -> List[AdvancedDryRunStep]:

    steps = []
    for s in matrix.scenarios:
        if s.enabled:
            steps.append(execute_advanced_dry_run_scenario(s))

    return steps

def validate_advanced_dry_run_steps(steps: List[AdvancedDryRunStep]) -> List[str]:
    errors = []
    for s in steps:
        if not s.dry_run:
            errors.append(f"Step {s.step_id} is not dry_run")
        if not s.local_fixture_only:
            errors.append(f"Step {s.step_id} is not local_fixture_only")
        if s.executed_real_side_effect:
            errors.append(f"Step {s.step_id} executed real side effect")
        if s.used_network:
            errors.append(f"Step {s.step_id} used network")
        if s.mutated_paper_state:
            errors.append(f"Step {s.step_id} mutated paper state")
        if s.used_broker:
            errors.append(f"Step {s.step_id} used broker")
        if s.created_order:
            errors.append(f"Step {s.step_id} created order")
        if s.sent_telegram:
            errors.append(f"Step {s.step_id} sent telegram")
        if s.deployed:
            errors.append(f"Step {s.step_id} deployed")
        if s.production_patch_applied:
            errors.append(f"Step {s.step_id} applied production patch")
    return errors

def advanced_dry_run_rehearsal_summary(steps: List[AdvancedDryRunStep]) -> Dict[str, Any]:
    return {
        "step_count": len(steps),
        "passed_count": sum(1 for s in steps if s.status == ReleaseCandidateStatus.PASSED),
        "failed_count": sum(1 for s in steps if s.status in [ReleaseCandidateStatus.FAILED, ReleaseCandidateStatus.BLOCKED]),
        "safe_count": sum(1 for s in steps if not s.executed_real_side_effect)
    }

def advanced_dry_run_rehearsal_to_text(steps: List[AdvancedDryRunStep], limit: int = 300) -> str:
    lines = ["Advanced Dry Run Steps:"]
    for s in steps[:limit]:
        lines.append(f" - {s.step_name}: {s.status.value}")
    return "\n".join(lines)
