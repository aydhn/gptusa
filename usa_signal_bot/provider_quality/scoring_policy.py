from typing import Dict
from usa_signal_bot.core.enums import DataQualityComponent

def build_default_provider_quality_scoring_policy() -> Dict[str, float]:
    return {
        "COMPLETENESS": 0.20,
        "FRESHNESS": 0.15,
        "SCHEMA_VALIDITY": 0.20,
        "CONTINUITY": 0.15,
        "SOURCE_AGREEMENT": 0.15,
        "OUTLIER_PROFILE": 0.05,
        "CACHE_RELIABILITY": 0.05,
        "SAFETY_COMPLIANCE": 0.05
    }

def validate_scoring_policy(policy: Dict[str, float]) -> list[str]:
    errors = []
    total_weight = sum(policy.values())
    if abs(total_weight - 1.0) > 0.01:
        errors.append(f"Scoring policy weights sum to {total_weight}, expected 1.0")
    for k, v in policy.items():
        if v < 0 or v > 1:
            errors.append(f"Weight for {k} is {v}, must be between 0 and 1")
    return errors

def normalize_scoring_weights(policy: Dict[str, float]) -> Dict[str, float]:
    total_weight = sum(policy.values())
    if total_weight == 0:
        return policy
    return {k: v / total_weight for k, v in policy.items()}

def scoring_policy_component_weight(component: DataQualityComponent, policy: Dict[str, float] | None = None) -> float:
    if policy is None:
        policy = build_default_provider_quality_scoring_policy()
    return policy.get(component.value, 0.0)

def scoring_policy_to_text(policy: Dict[str, float]) -> str:
    lines = ["Scoring Policy Weights:"]
    for k, v in policy.items():
        lines.append(f"  {k}: {v:.2f}")
    return "\n".join(lines)
