from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    ClosureBlocker, BacktestClosureRiskFlag, BacktestBandPhase
)

def blocker_from_risk_flag(flag: BacktestClosureRiskFlag, message: str, source_phase: BacktestBandPhase | None = None) -> ClosureBlocker:
    return ClosureBlocker(
        blocker_name=flag.name,
        blocker_detected=True,
        severity="CRITICAL",
        message=message,
        source_phase=source_phase,
        risk_flag=flag,
        resolution_hint="Review documentation and ensure constraints are met."
    )

def detect_closure_blockers(final_audit_inputs: dict[str, Any]) -> list[ClosureBlocker]:
    blockers = []

    # Check ingestion
    ingestion = final_audit_inputs.get("ingestion")
    if ingestion and not ingestion.valid_for_phase152:
        blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.PHASE151_NOT_READY, "Phase 151 ingestion not valid"))

    # Check safety audits
    safety = final_audit_inputs.get("safety_audit")
    if safety and not safety.audit_passed:
        blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.SAFETY_COMPLIANCE_FAILED, "Safety audit failed"))

    research = final_audit_inputs.get("research_boundary_audit")
    if research and not research.audit_passed:
        blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.RESEARCH_BOUNDARY_FAILED, "Research boundary audit failed"))

    # Check lineage/determinism
    manifest = final_audit_inputs.get("artifact_lineage")
    if manifest and not manifest.manifest_valid:
         blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.ARTIFACT_LINEAGE_INVALID, "Artifact lineage invalid"))

    determinism = final_audit_inputs.get("determinism_audit")
    if determinism and not determinism.audit_passed:
         blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.DETERMINISM_COMPLIANCE_FAILED, "Determinism compliance failed"))

    return blockers

def has_blocking_closure_issue(blockers: list[ClosureBlocker]) -> bool:
    return any(b.blocker_detected for b in blockers)

def closure_blockers_summary(blockers: list[ClosureBlocker]) -> dict[str, Any]:
    return {"count": len(blockers), "has_blockers": has_blocking_closure_issue(blockers)}

def closure_blockers_to_text(blockers: list[ClosureBlocker], limit: int = 300) -> str:
    return f"ClosureBlockers(count={len(blockers)}, has_blockers={has_blocking_closure_issue(blockers)})"
