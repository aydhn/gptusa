from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingCapFloorRule, SizingPolicy, SizingPrototypeResult, SizingCapFloorRuleKind

def build_sizing_cap_floor_rules(results: list[SizingPrototypeResult], policy: SizingPolicy) -> list[SizingCapFloorRule]:
    rules = []
    for r in results:
        # Max prototype fraction rule
        max_rule = SizingCapFloorRule(
            rule_kind=SizingCapFloorRuleKind.MAX_PROTOTYPE_EXPOSURE_FRACTION,
            name="Max Prototype Exposure",
            required=True,
            passed=True,
            expected_value=policy.max_prototype_fraction,
            observed_value=r.raw_prototype_fraction,
            applies_to_symbol=r.symbol,
            applies_to_method=r.method_kind,
            rationale="Enforce max prototype fraction."
        )
        if r.raw_prototype_fraction is not None and r.raw_prototype_fraction > policy.max_prototype_fraction:
            max_rule.passed = False
        rules.append(max_rule)

        # Min prototype fraction rule
        min_rule = SizingCapFloorRule(
            rule_kind=SizingCapFloorRuleKind.MIN_PROTOTYPE_EXPOSURE_FRACTION,
            name="Min Prototype Exposure",
            required=True,
            passed=True,
            expected_value=policy.min_prototype_fraction,
            observed_value=r.raw_prototype_fraction,
            applies_to_symbol=r.symbol,
            applies_to_method=r.method_kind,
            rationale="Enforce min prototype fraction."
        )
        if r.raw_prototype_fraction is not None and r.raw_prototype_fraction < policy.min_prototype_fraction:
            min_rule.passed = False
        rules.append(min_rule)
    return rules

def apply_sizing_cap_floor_rules(results: list[SizingPrototypeResult], policy: SizingPolicy) -> list[SizingPrototypeResult]:
    for r in results:
        if r.raw_prototype_fraction is None:
            r.capped_prototype_fraction = None
            continue

        capped = max(policy.min_prototype_fraction, min(policy.max_prototype_fraction, r.raw_prototype_fraction))
        r.capped_prototype_fraction = capped
        r.cap_floor_applied = (capped != r.raw_prototype_fraction)
    return results

def validate_sizing_cap_floor_rules(items: list[SizingCapFloorRule]) -> list[str]:
    errors = []
    return errors

def sizing_cap_floor_rules_summary(items: list[SizingCapFloorRule]) -> dict[str, Any]:
    return {"count": len(items), "valid": len(validate_sizing_cap_floor_rules(items)) == 0}

def sizing_cap_floor_rules_to_text(items: list[SizingCapFloorRule], limit: int = 300) -> str:
    return f"Sizing Cap/Floor Rules: {len(items)}"[:limit]
