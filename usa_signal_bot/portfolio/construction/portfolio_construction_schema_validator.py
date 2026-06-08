from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioConstructionInputReference,
    PortfolioSandboxCandidate,
    PortfolioConstructionPolicy,
    SandboxAllocationMethodContract,
    SandboxAllocationResult,
    PrototypeExposureTable,
    AllocationSandboxComparisonReport,
    PortfolioConstructionContext
)

def validate_construction_input_reference_schema(item: PortfolioConstructionInputReference) -> List[str]:
    errors = []
    if not item.input_ref_id:
        errors.append("Missing input_ref_id.")
    if not item.source_artifact_name:
        errors.append("Missing source_artifact_name.")
    return errors

def validate_portfolio_sandbox_candidate_schema(item: PortfolioSandboxCandidate) -> List[str]:
    errors = []
    if not item.candidate_id:
        errors.append("Missing candidate_id.")
    if not item.symbol:
        errors.append("Missing symbol.")
    return errors

def validate_portfolio_construction_policy_schema(item: PortfolioConstructionPolicy) -> List[str]:
    errors = []
    if not item.policy_id:
        errors.append("Missing policy_id.")
    if item.max_sandbox_weight_fraction is None:
        errors.append("Missing max_sandbox_weight_fraction.")
    return errors

def validate_sandbox_allocation_method_contract_schema(item: SandboxAllocationMethodContract) -> List[str]:
    errors = []
    if not item.contract_id:
        errors.append("Missing contract_id.")
    return errors

def validate_sandbox_allocation_result_schema(item: SandboxAllocationResult) -> List[str]:
    errors = []
    if not item.result_id:
        errors.append("Missing result_id.")
    if not item.symbol:
        errors.append("Missing symbol.")
    return errors

def validate_prototype_exposure_table_schema(table: PrototypeExposureTable) -> List[str]:
    errors = []
    if not table.table_id:
        errors.append("Missing table_id.")
    return errors

def validate_allocation_sandbox_comparison_report_schema(report: AllocationSandboxComparisonReport) -> List[str]:
    errors = []
    if not report.report_id:
        errors.append("Missing report_id.")
    return errors

def validate_portfolio_construction_context_schema(context: PortfolioConstructionContext) -> List[str]:
    errors = []
    if not context.context_id:
        errors.append("Missing context_id.")
    return errors

def validate_portfolio_construction_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_portfolio_construction_columns(columns)

def validate_no_forbidden_portfolio_construction_columns(columns: List[str]) -> List[str]:
    forbidden = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "portfolio_weight",
        "target_weight", "actual_target_weight", "actual_portfolio_weight",
        "allocation", "actual_allocation", "capital_allocation",
        "actual_position_size", "position_size", "order_size", "real_order",
        "live_signal", "buy_signal", "sell_signal", "recommended_weight",
        "production_patch"
    ]
    return [col for col in columns if col in forbidden]

def portfolio_construction_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"valid": len(errors) == 0, "error_count": len(errors)}

def portfolio_construction_schema_to_text(errors: List[str]) -> str:
    if not errors:
        return "Schema valid."
    return "Schema errors:\n" + "\n".join(f"- {e}" for e in errors)
