from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    PositionSizingBoundaryContract, PositionSizingBoundaryRule, PositionSizingBoundaryKind
)

def build_position_sizing_boundary_rules() -> list[PositionSizingBoundaryRule]:
    rules = []

    kinds = [
        PositionSizingBoundaryKind.NO_ACTUAL_POSITION_SIZE_PHASE153,
        PositionSizingBoundaryKind.NO_TARGET_WEIGHT_PHASE153,
        PositionSizingBoundaryKind.NO_ALLOCATION_PHASE153,
        PositionSizingBoundaryKind.NO_CAPITAL_DEPLOYMENT_PHASE153,
        PositionSizingBoundaryKind.NO_ORDER_SIZE_PHASE153,
        PositionSizingBoundaryKind.SIZING_PROTOTYPE_ALLOWED_PHASE154
    ]

    for kind in kinds:
        rule = PositionSizingBoundaryRule()
        rule.boundary_kind = kind
        rule.name = kind.value
        rule.passed = True
        rules.append(rule)

    return rules

def build_position_sizing_boundary_contract() -> PositionSizingBoundaryContract:
    contract = PositionSizingBoundaryContract()
    contract.rules = build_position_sizing_boundary_rules()
    contract.boundary_valid = all(r.passed for r in contract.rules)
    return contract

def validate_position_sizing_boundary_contract(boundary: PositionSizingBoundaryContract) -> list[str]:
    errors = []
    if not boundary.no_actual_position_size_phase153:
        errors.append("no_actual_position_size_phase153 must be True")
    if not boundary.no_target_weight_phase153:
        errors.append("no_target_weight_phase153 must be True")
    if not boundary.no_allocation_phase153:
        errors.append("no_allocation_phase153 must be True")
    if not boundary.no_capital_deployment_phase153:
        errors.append("no_capital_deployment_phase153 must be True")
    if not boundary.no_order_size_phase153:
        errors.append("no_order_size_phase153 must be True")
    return errors

def position_sizing_boundary_summary(boundary: PositionSizingBoundaryContract) -> dict[str, Any]:
    return {
        "rule_count": len(boundary.rules),
        "valid": boundary.boundary_valid
    }

def position_sizing_boundary_to_text(boundary: PositionSizingBoundaryContract, limit: int = 300) -> str:
    return f"PositionSizingBoundaryContract: {len(boundary.rules)} rules, valid: {boundary.boundary_valid}"
