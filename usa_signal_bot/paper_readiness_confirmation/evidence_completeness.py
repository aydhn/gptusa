from typing import Any

def required_confirmation_evidence_types() -> list[str]:
    return [
        "firewall_audit_review",
        "firewall_replay_result",
        "zero_mutation_audit",
        "readiness_audit_checkpoint",
        "activation_denied_checkpoint",
        "pre_paper_rehearsal_review",
        "final_handoff_full_review",
        "sealed_readiness_archive",
        "readiness_rehearsal_review",
        "promotion_dossier_review",
        "observer_governance_review",
        "validation_reports",
        "audit_trails"
    ]

def collect_confirmation_evidence_refs(firewall_audit_payload: dict[str, Any]) -> list[str]:
    refs = []
    if firewall_audit_payload:
        refs.append("firewall_audit_review_present")
        if firewall_audit_payload.get("zero_mutation_audit"):
            refs.append("zero_mutation_audit_present")
    return refs

def evaluate_confirmation_evidence_completeness(firewall_audit_payload: dict[str, Any]) -> dict[str, Any]:
    missing = missing_confirmation_evidence_types(firewall_audit_payload)
    stale = stale_confirmation_evidence_types(firewall_audit_payload)

    return {
        "is_complete": len(missing) == 0 and len(stale) == 0,
        "missing": missing,
        "stale": stale
    }

def missing_confirmation_evidence_types(firewall_audit_payload: dict[str, Any]) -> list[str]:
    missing = []
    if not firewall_audit_payload:
        missing.append("firewall_audit_review")
    else:
        if not firewall_audit_payload.get("zero_mutation_audit"):
             missing.append("zero_mutation_audit")
        if not firewall_audit_payload.get("firewall_replay_result"):
             missing.append("firewall_replay_result")
    return missing

def stale_confirmation_evidence_types(firewall_audit_payload: dict[str, Any]) -> list[str]:
    stale = []
    if firewall_audit_payload:
         refresh = firewall_audit_payload.get("pre_paper_evidence_refresh", {})
         if refresh and refresh.get("status") != "FRESH":
              stale.append("evidence_stale")
    return stale

def evidence_completeness_to_text(payload: dict[str, Any]) -> str:
    comp = evaluate_confirmation_evidence_completeness(payload)
    return f"Evidence Complete: {comp['is_complete']}"
