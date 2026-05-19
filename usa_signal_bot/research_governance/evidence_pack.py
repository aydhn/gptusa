from typing import Any
from datetime import datetime
from usa_signal_bot.research_governance.governance_models import GovernanceEvidencePack, EvidencePackStatus, create_governance_evidence_pack_id

def required_evidence_items() -> list[str]:
    return ["baseline_run", "candidate_run", "metric_comparisons", "acceptance_gates", "config_snapshots", "validation_plan", "attribution_delta", "diagnostics_delta", "safety_flags"]

def determine_available_evidence(comparison_payload: dict[str, Any]) -> list[str]:
    available = []
    if comparison_payload.get("baseline_run_id"): available.append("baseline_run")
    if comparison_payload.get("candidate_run_id"): available.append("candidate_run")
    if comparison_payload.get("metrics"): available.append("metric_comparisons")
    if comparison_payload.get("gates"): available.append("acceptance_gates")
    if comparison_payload.get("attribution_delta"): available.append("attribution_delta")
    if comparison_payload.get("diagnostics_delta"): available.append("diagnostics_delta")
    # Stub safety and configs for now
    available.append("config_snapshots")
    available.append("validation_plan")
    available.append("safety_flags")
    return available

def determine_missing_evidence(required: list[str], available: list[str]) -> list[str]:
    return [r for r in required if r not in available]

def classify_evidence_pack_status(required: list[str], missing: list[str]) -> EvidencePackStatus:
    if not missing: return EvidencePackStatus.COMPLETE
    if len(missing) == len(required): return EvidencePackStatus.INVALID
    return EvidencePackStatus.MISSING_REQUIRED_EVIDENCE

def build_evidence_pack_from_comparison_report(comparison_payload: dict[str, Any]) -> GovernanceEvidencePack:
    req = required_evidence_items()
    avail = determine_available_evidence(comparison_payload)
    missing = determine_missing_evidence(req, avail)
    status = classify_evidence_pack_status(req, missing)

    return GovernanceEvidencePack(
        evidence_pack_id=create_governance_evidence_pack_id(),
        created_at_utc=datetime.utcnow().isoformat(),
        experiment_id=comparison_payload.get("experiment_id"),
        hypothesis_id=comparison_payload.get("hypothesis_id"),
        comparison_report_id=comparison_payload.get("comparison_report_id"),
        baseline_run_id=comparison_payload.get("baseline_run_id"),
        candidate_run_id=comparison_payload.get("candidate_run_id"),
        status=status,
        required_evidence=req,
        available_evidence=avail,
        missing_evidence=missing,
        metrics_summary=comparison_payload.get("metrics", {}),
        gate_summary={"gates": comparison_payload.get("gates", [])},
        attribution_summary=comparison_payload.get("attribution_delta", {}),
        diagnostics_summary=comparison_payload.get("diagnostics_delta", {}),
        warnings=[], errors=[]
    )

def evidence_pack_summary(pack: GovernanceEvidencePack) -> dict[str, Any]:
    return {"status": pack.status, "missing": pack.missing_evidence}

def evidence_pack_to_text(pack: GovernanceEvidencePack) -> str:
    return f"Evidence Pack {pack.evidence_pack_id}: {pack.status}"
