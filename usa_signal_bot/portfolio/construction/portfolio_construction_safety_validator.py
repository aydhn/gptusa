import pandas as pd
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioConstructionContext,
    PortfolioConstructionPolicy,
    SandboxAllocationMethodContract,
    SandboxAllocationResult,
    PrototypeExposureTable,
    AllocationSandboxComparisonReport,
    AllocationSandboxSafetyBoundaryResult,
    Phase156ReadinessGate
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def validate_portfolio_construction_context_safety(context: PortfolioConstructionContext) -> List[str]:
    errors = []

    checks = [
        ("live_trading_enabled", PortfolioConstructionRiskFlag.LIVE_TRADING_RISK),
        ("paper_trading_enabled", PortfolioConstructionRiskFlag.PAPER_TRADING_RISK),
        ("broker_execution_enabled", PortfolioConstructionRiskFlag.BROKER_RISK),
        ("real_order_creation_enabled", PortfolioConstructionRiskFlag.REAL_ORDER_RISK),
        ("paper_state_mutation_enabled", PortfolioConstructionRiskFlag.PAPER_MUTATION_RISK),
        ("strategy_activation_allowed", PortfolioConstructionRiskFlag.STRATEGY_ACTIVATION_RISK),
        ("actual_target_weights_produced", PortfolioConstructionRiskFlag.ACTUAL_TARGET_WEIGHT_RISK),
        ("actual_portfolio_weights_produced", PortfolioConstructionRiskFlag.ACTUAL_PORTFOLIO_WEIGHT_RISK),
        ("actual_allocation_produced", PortfolioConstructionRiskFlag.ACTUAL_ALLOCATION_RISK),
        ("actual_position_size_produced", PortfolioConstructionRiskFlag.ACTUAL_POSITION_SIZE_RISK),
        ("order_size_produced", PortfolioConstructionRiskFlag.ORDER_SIZE_RISK),
        ("capital_deployment_allowed", PortfolioConstructionRiskFlag.CAPITAL_DEPLOYMENT_RISK),
        ("portfolio_optimization_enabled", PortfolioConstructionRiskFlag.PORTFOLIO_OPTIMIZATION_RISK),
    ]

    for attr, flag in checks:
        if getattr(context, attr, False):
            errors.append(f"Context {attr} is True.")
            context.risk_flags.append(flag)

    return errors

def validate_portfolio_construction_policy_safety(policy: PortfolioConstructionPolicy) -> List[str]:
    from usa_signal_bot.portfolio.construction.portfolio_construction_policy import validate_portfolio_construction_policy
    return validate_portfolio_construction_policy(policy)

def validate_sandbox_allocation_method_contract_safety(contract: SandboxAllocationMethodContract) -> List[str]:
    from usa_signal_bot.portfolio.construction.sandbox_allocation_method_contracts import validate_sandbox_allocation_method_contracts
    return validate_sandbox_allocation_method_contracts([contract])

def validate_sandbox_allocation_results_safety(items: List[SandboxAllocationResult]) -> List[str]:
    from usa_signal_bot.portfolio.construction.equal_sandbox_allocation import validate_equal_sandbox_allocation
    return validate_equal_sandbox_allocation(items)

def validate_prototype_exposure_table_safety(table: PrototypeExposureTable) -> List[str]:
    from usa_signal_bot.portfolio.construction.prototype_exposure_table import validate_prototype_exposure_table
    return validate_prototype_exposure_table(table)

def validate_allocation_sandbox_report_safety(report: AllocationSandboxComparisonReport) -> List[str]:
    from usa_signal_bot.portfolio.construction.allocation_sandbox_comparison_report import validate_allocation_sandbox_comparison_report
    return validate_allocation_sandbox_comparison_report(report)

def validate_allocation_sandbox_safety_boundary_safety(boundary: AllocationSandboxSafetyBoundaryResult) -> List[str]:
    from usa_signal_bot.portfolio.construction.allocation_sandbox_safety_boundary import validate_allocation_sandbox_safety_boundary_result
    return validate_allocation_sandbox_safety_boundary_result(boundary)

def validate_phase156_readiness_gate_safety(gate: Phase156ReadinessGate) -> List[str]:
    from usa_signal_bot.portfolio.construction.phase156_readiness_gate import validate_phase156_readiness_gate
    return validate_phase156_readiness_gate(gate)

def validate_portfolio_construction_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    from usa_signal_bot.portfolio.construction.portfolio_construction_schema_validator import validate_no_forbidden_portfolio_construction_columns
    if df is None or df.empty:
        return []
    return validate_no_forbidden_portfolio_construction_columns(df.columns.tolist())

def portfolio_construction_text_has_trade_or_execution_language(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()
    unsafe_terms = [
        "execute order", "send order", "place trade", "live trading",
        "activate strategy", "actual target weight", "actual portfolio weight",
        "deploy capital", "order size", "buy signal", "sell signal"
    ]

    for term in unsafe_terms:
        if term in text_lower:
            # check context - allow if negated
            if f"no {term}" not in text_lower and f"not {term}" not in text_lower and f"without {term}" not in text_lower and f"no actual target weight" not in text_lower and f"no actual allocation" not in text_lower:
                return True

    return False

def portfolio_construction_payload_has_forbidden_fields(payload: Dict[str, Any]) -> bool:
    from usa_signal_bot.portfolio.construction.portfolio_construction_input_resolver import detect_forbidden_construction_fields
    return len(detect_forbidden_construction_fields(payload)) > 0

def collect_portfolio_construction_risk_flags(context: Optional[PortfolioConstructionContext] = None) -> List[PortfolioConstructionRiskFlag]:
    if not context:
        return []

    flags = set(context.risk_flags)
    flags.update(context.ingestion.risk_flags)

    list_attrs = [
        "input_references", "candidates", "method_contracts",
        "scores", "allocation_results", "diagnostics"
    ]
    for attr in list_attrs:
        for item in getattr(context, attr, []):
            flags.update(item.risk_flags)

    scalar_attrs = [
        "policy", "exposure_table", "comparison_report",
        "validation_report", "safety_boundary", "phase156_readiness_gate"
    ]
    for attr in scalar_attrs:
        item = getattr(context, attr, None)
        if item:
            flags.update(item.risk_flags)

    return list(flags)

def portfolio_construction_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors)}

def portfolio_construction_safety_to_text(errors: List[str]) -> str:
    if not errors:
        return "Safety validation passed."
    return "Safety errors:\n" + "\n".join(f"- {e}" for e in errors)
