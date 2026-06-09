from typing import Any, Dict, List, Optional
import hashlib
import json

from usa_signal_bot.release.phase159_models import (
    ReleaseCandidateRiskRegister,
    ReleaseCandidateRiskItem,
    AcceptanceAreaReport,
    AdvancedDryRunStep,
    ReleaseCandidateRiskLevel,
    AcceptanceAreaKind,
    ReleaseCandidateStatus,
    AdvancedAcceptanceRiskFlag,
    create_release_candidate_risk_item_id,
    create_release_candidate_risk_register_id,
    generate_timestamp
)

def build_release_candidate_risk_items(area_reports: List[AcceptanceAreaReport], steps: List[AdvancedDryRunStep]) -> List[ReleaseCandidateRiskItem]:
    items = []

    for report in area_reports:
        if not report.passed:
            items.append(ReleaseCandidateRiskItem(
                risk_id=create_release_candidate_risk_item_id(),
                created_at_utc=generate_timestamp(),
                title=f"Failed Area Report: {report.title}",
                risk_level=ReleaseCandidateRiskLevel.BLOCKING,
                area_kind=report.area_kind,
                blocking=True,
                detected=True,
                mitigation="Fix the underlying failures in this area before proceeding.",
                evidence_ref=report.report_id,
                warnings=[],
                errors=[],
                risk_flags=[AdvancedAcceptanceRiskFlag.RELEASE_CANDIDATE_RISK_BLOCKING],
                metadata={}
            ))

    for step in steps:
        if step.status != ReleaseCandidateStatus.PASSED:
            items.append(ReleaseCandidateRiskItem(
                risk_id=create_release_candidate_risk_item_id(),
                created_at_utc=generate_timestamp(),
                title=f"Failed Dry Run Step: {step.step_name}",
                risk_level=ReleaseCandidateRiskLevel.BLOCKING,
                area_kind=step.area_kind,
                blocking=True,
                detected=True,
                mitigation="Fix the underlying step execution failure.",
                evidence_ref=step.step_id,
                warnings=[],
                errors=[],
                risk_flags=[AdvancedAcceptanceRiskFlag.ADVANCED_DRY_RUN_FAILED],
                metadata={}
            ))

    # Add explicit check for execution indicators in steps
    for step in steps:
        if step.executed_real_side_effect or step.used_broker or step.mutated_paper_state or step.deployed:
            items.append(ReleaseCandidateRiskItem(
                risk_id=create_release_candidate_risk_item_id(),
                created_at_utc=generate_timestamp(),
                title=f"Execution Violation in Step: {step.step_name}",
                risk_level=ReleaseCandidateRiskLevel.BLOCKING,
                area_kind=step.area_kind,
                blocking=True,
                detected=True,
                mitigation="Ensure dry_run and local_fixture_only flags are respected.",
                evidence_ref=step.step_id,
                warnings=[],
                errors=[],
                risk_flags=[AdvancedAcceptanceRiskFlag.RELEASE_CANDIDATE_RISK_BLOCKING],
                metadata={}
            ))

    return items

def compute_release_candidate_risk_register_hash(register: ReleaseCandidateRiskRegister) -> str:
    data = []
    for item in register.risks:
        data.append({
            "title": item.title,
            "level": item.risk_level.value,
            "blocking": item.blocking
        })
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def validate_release_candidate_risk_register(register: ReleaseCandidateRiskRegister) -> List[str]:
    errors = []
    if register.blocking_risk_count > 0 and register.register_valid and not register.release_candidate_blocked:
        errors.append("Register has blocking risks but is not marked as blocked")
    return errors

def build_release_candidate_risk_register(area_reports: List[AcceptanceAreaReport], steps: List[AdvancedDryRunStep]) -> ReleaseCandidateRiskRegister:
    items = build_release_candidate_risk_items(area_reports, steps)

    blocking_count = sum(1 for i in items if i.blocking)
    high_critical = sum(1 for i in items if i.risk_level in [ReleaseCandidateRiskLevel.HIGH, ReleaseCandidateRiskLevel.CRITICAL])

    register = ReleaseCandidateRiskRegister(
        register_id=create_release_candidate_risk_register_id(),
        created_at_utc=generate_timestamp(),
        risks=items,
        risk_count=len(items),
        blocking_risk_count=blocking_count,
        high_or_critical_count=high_critical,
        register_hash=None,
        register_valid=True,
        release_candidate_blocked=blocking_count > 0,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    register.register_hash = compute_release_candidate_risk_register_hash(register)

    if blocking_count > 0:
        register.risk_flags.append(AdvancedAcceptanceRiskFlag.RELEASE_CANDIDATE_RISK_BLOCKING)

    return register

def release_candidate_risk_register_to_text(register: ReleaseCandidateRiskRegister, limit: int = 300) -> str:
    lines = [f"Risk Register: {register.register_id}", f"Blocked: {register.release_candidate_blocked}"]
    for r in register.risks[:limit]:
        lines.append(f" - {r.title} [{r.risk_level.value}] (Blocking: {r.blocking})")
    return "\n".join(lines)
