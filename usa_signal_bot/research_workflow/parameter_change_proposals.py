from typing import Any, List, Optional
import datetime
from .workflow_models import ParameterChangeProposal, RepairQueueItem, create_parameter_change_proposal_id

def create_parameter_change_proposal(
    target_module: Optional[str],
    target_strategy: Optional[str],
    parameter_name: str,
    baseline_value: Any,
    candidate_value: Any,
    change_reason: str,
    expected_effect: str
) -> ParameterChangeProposal:
    proposal_id = create_parameter_change_proposal_id(parameter_name)
    now_utc = datetime.datetime.utcnow().isoformat() + "Z"

    return ParameterChangeProposal(
        proposal_id=proposal_id,
        created_at_utc=now_utc,
        target_module=target_module,
        target_strategy=target_strategy,
        parameter_name=parameter_name,
        baseline_value=baseline_value,
        candidate_value=candidate_value,
        change_reason=change_reason,
        expected_effect=expected_effect,
        risk_notes=["Local research only. Not auto-applied."],
        allowed_for_auto_apply=False,
        warnings=[],
        errors=[],
        metadata={}
    )

def parameter_change_from_repair_item(item: RepairQueueItem) -> List[ParameterChangeProposal]:
    # Placeholder mapping from a repair item to a generic proposal
    if item.target_name:
        return [create_parameter_change_proposal(
            target_module="unknown",
            target_strategy=item.target_name,
            parameter_name="TBD_PARAMETER",
            baseline_value="CURRENT",
            candidate_value="PROPOSED",
            change_reason=item.suggested_safe_action,
            expected_effect="Mitigate failure mode"
        )]
    return []

def validate_parameter_change_safe(proposal: ParameterChangeProposal) -> List[str]:
    warnings = []
    if proposal.allowed_for_auto_apply:
        warnings.append("Unsafe: allowed_for_auto_apply must be False")
    return warnings

def parameter_change_summary(proposals: List[ParameterChangeProposal]) -> dict[str, Any]:
    return {
        "total_proposals": len(proposals),
        "by_strategy": {p.target_strategy: len([x for x in proposals if x.target_strategy == p.target_strategy]) for p in proposals if p.target_strategy}
    }

def parameter_change_proposals_to_text(proposals: List[ParameterChangeProposal], limit: int = 100) -> str:
    lines = [f"Parameter Proposals: {len(proposals)}", "-"*40]
    for p in proposals[:limit]:
        lines.append(f"[{p.target_strategy}] {p.parameter_name}: {p.baseline_value} -> {p.candidate_value}")
    if len(proposals) > limit:
        lines.append(f"... and {len(proposals)-limit} more.")
    return "\n".join(lines)
