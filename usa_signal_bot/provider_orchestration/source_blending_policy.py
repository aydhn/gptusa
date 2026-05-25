from typing import Any
from usa_signal_bot.core.enums import SourceBlendMethod

def build_default_source_blending_policy() -> dict[str, Any]:
    return {
        "allow_blending": True,
        "min_sources_for_blending": 2,
        "default_method": "TRUST_WEIGHTED_BLEND",
        "max_disagreement_for_blending": 0.25,
        "produces_trade_signal": False,
        "produces_order_decision": False,
        "dry_run_only": True,
        "research_data_only": True
    }

def validate_source_blending_policy(policy: dict[str, Any]) -> list[str]:
    errors = []
    if policy.get("produces_trade_signal", True):
        errors.append("produces_trade_signal must be False")
    if policy.get("produces_order_decision", True):
        errors.append("produces_order_decision must be False")
    if not policy.get("dry_run_only", False):
        errors.append("dry_run_only must be True")
    if not policy.get("research_data_only", False):
        errors.append("research_data_only must be True")
    return errors

def source_blending_method_from_inputs(source_count: int, disagreement_score: float | None = None, allow_blending: bool = True) -> SourceBlendMethod:
    if not allow_blending:
        return SourceBlendMethod.NO_BLEND
    if source_count < 2:
        return SourceBlendMethod.PRIMARY_ONLY
    if disagreement_score is not None and disagreement_score > 0.25:
        return SourceBlendMethod.PRIMARY_ONLY
    return SourceBlendMethod.TRUST_WEIGHTED_BLEND

def source_blending_policy_to_text(policy: dict[str, Any]) -> str:
    lines = ["--- Source Blending Policy ---"]
    for k, v in policy.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)
