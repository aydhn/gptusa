from typing import Any
import pandas as pd
from usa_signal_bot.portfolio.sizing.phase154_models import (
    SizingPrototypeContext, SizingPolicy, SizingMethodContract,
    SizingPrototypeResult, SizingComparisonMatrix, SizingSafetyBoundaryResult,
    Phase155ReadinessGate, SizingPrototypeRiskFlag
)
from usa_signal_bot.portfolio.sizing.sizing_input_resolver import FORBIDDEN_SIZING_COLUMNS

def validate_sizing_context_safety(context: SizingPrototypeContext) -> list[str]:
    checks = [
        ("live_trading_enabled", "Live trading is enabled."),
        ("paper_trading_enabled", "Paper trading is enabled."),
        ("broker_execution_enabled", "Broker execution is enabled."),
        ("actual_position_sizing_executed", "Actual position sizing executed."),
        ("target_weights_produced", "Target weights produced."),
        ("allocation_output_produced", "Allocation output produced."),
        ("capital_deployment_allowed", "Capital deployment allowed."),
        ("deployment_allowed", "Deployment allowed."),
        ("network_used", "Network fetching is enabled."),
        ("paid_api_used", "Paid API is enabled."),
        ("scraping_used", "Scraping is enabled.")
    ]

    return [msg for attr, msg in checks if getattr(context, attr, False)]

def validate_sizing_policy_safety(policy: SizingPolicy) -> list[str]:
    errors = []
    if policy.actual_position_sizing_allowed: errors.append("actual_position_sizing_allowed is True.")
    if policy.target_weights_allowed: errors.append("target_weights_allowed is True.")
    return errors

def validate_sizing_method_contract_safety(contract: SizingMethodContract) -> list[str]:
    errors = []
    if contract.produces_actual_position_size: errors.append("produces_actual_position_size is True.")
    if contract.produces_target_weight: errors.append("produces_target_weight is True.")
    return errors

def validate_sizing_prototype_results_safety(items: list[SizingPrototypeResult]) -> list[str]:
    errors = []
    for i, item in enumerate(items):
        if item.actual_position_size is not None: errors.append(f"Result {i} produces actual position size.")
        if item.target_weight is not None: errors.append(f"Result {i} produces target weight.")
    return errors

def validate_sizing_comparison_matrix_safety(matrix: SizingComparisonMatrix) -> list[str]:
    errors = []
    if not matrix.no_actual_position_size: errors.append("Matrix allows actual position size.")
    return errors

def validate_sizing_safety_boundary_safety(boundary: SizingSafetyBoundaryResult) -> list[str]:
    errors = []
    if not boundary.boundary_passed: errors.append("Safety boundary failed.")
    return errors

def validate_phase155_readiness_gate_safety(gate: Phase155ReadinessGate) -> list[str]:
    errors = []
    if not gate.ready_for_phase155: errors.append("Phase155 gate failed.")
    return errors

def validate_sizing_dataframe_output_safety(df: pd.DataFrame) -> list[str]:
    errors = []
    cols = df.columns.tolist()
    for col in cols:
        if col.lower() in FORBIDDEN_SIZING_COLUMNS:
            errors.append(f"Forbidden column in DataFrame: {col}")
    return errors

def sizing_text_has_trade_or_execution_language(text: str) -> bool:
    forbidden = ["buy", "sell", "execution", "execute trade", "submit order", "live run"]
    t = text.lower()
    return any(f in t for f in forbidden)

def sizing_payload_has_forbidden_fields(payload: dict[str, Any]) -> bool:
    payload_str = str(payload).lower()
    return any(f in payload_str for f in FORBIDDEN_SIZING_COLUMNS)

def collect_sizing_risk_flags(context: SizingPrototypeContext | None = None) -> list[SizingPrototypeRiskFlag]:
    flags = []
    if context:
        flags.extend(context.risk_flags)
    return list(set(flags))

def sizing_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors)}

def sizing_safety_to_text(errors: list[str]) -> str:
    if errors:
         return f"Safety validation failed: {errors[0]}"
    return "Safety valid."
