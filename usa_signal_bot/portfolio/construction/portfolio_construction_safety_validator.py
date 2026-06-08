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

    if context.live_trading_enabled:
        errors.append("Context live_trading_enabled is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.LIVE_TRADING_RISK)
    if context.paper_trading_enabled:
        errors.append("Context paper_trading_enabled is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.PAPER_TRADING_RISK)
    if context.broker_execution_enabled:
        errors.append("Context broker_execution_enabled is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.BROKER_RISK)
    if context.real_order_creation_enabled:
        errors.append("Context real_order_creation_enabled is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.REAL_ORDER_RISK)
    if context.paper_state_mutation_enabled:
        errors.append("Context paper_state_mutation_enabled is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.PAPER_MUTATION_RISK)
    if context.strategy_activation_allowed:
        errors.append("Context strategy_activation_allowed is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.STRATEGY_ACTIVATION_RISK)
    if context.actual_target_weights_produced:
        errors.append("Context actual_target_weights_produced is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_TARGET_WEIGHT_RISK)
    if context.actual_portfolio_weights_produced:
        errors.append("Context actual_portfolio_weights_produced is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_PORTFOLIO_WEIGHT_RISK)
    if context.actual_allocation_produced:
        errors.append("Context actual_allocation_produced is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_ALLOCATION_RISK)
    if context.actual_position_size_produced:
        errors.append("Context actual_position_size_produced is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_POSITION_SIZE_RISK)
    if context.order_size_produced:
        errors.append("Context order_size_produced is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.ORDER_SIZE_RISK)
    if context.capital_deployment_allowed:
        errors.append("Context capital_deployment_allowed is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.CAPITAL_DEPLOYMENT_RISK)
    if context.portfolio_optimization_enabled:
        errors.append("Context portfolio_optimization_enabled is True.")
        context.risk_flags.append(PortfolioConstructionRiskFlag.PORTFOLIO_OPTIMIZATION_RISK)

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

    for ref in context.input_references:
        flags.update(ref.risk_flags)
    for c in context.candidates:
        flags.update(c.risk_flags)
    if context.policy:
        flags.update(context.policy.risk_flags)
    for m in context.method_contracts:
        flags.update(m.risk_flags)
    for s in context.scores:
        flags.update(s.risk_flags)
    for r in context.allocation_results:
        flags.update(r.risk_flags)
    if context.exposure_table:
        flags.update(context.exposure_table.risk_flags)
    for d in context.diagnostics:
        flags.update(d.risk_flags)
    if context.comparison_report:
        flags.update(context.comparison_report.risk_flags)
    if context.validation_report:
        flags.update(context.validation_report.risk_flags)
    if context.safety_boundary:
        flags.update(context.safety_boundary.risk_flags)
    if context.phase156_readiness_gate:
        flags.update(context.phase156_readiness_gate.risk_flags)

    return list(flags)

def portfolio_construction_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors)}

def portfolio_construction_safety_to_text(errors: List[str]) -> str:
    if not errors:
        return "Safety validation passed."
    return "Safety errors:\n" + "\n".join(f"- {e}" for e in errors)
