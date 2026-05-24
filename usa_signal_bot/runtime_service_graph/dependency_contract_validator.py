from typing import Any, Dict, List
from usa_signal_bot.runtime_service_graph.phase103_models import DependencyContract

def validate_dependency_contract_safety(contract: DependencyContract) -> List[str]:
    errors = []

    if contract.allows_execution:
        errors.append("Contract permits execution")
    if contract.allows_broker:
        errors.append("Contract permits broker interaction")
    if contract.allows_order:
        errors.append("Contract permits order creation")
    if contract.allows_paper_mutation:
        errors.append("Contract permits paper state mutation")
    if contract.allows_telegram_real_send:
        errors.append("Contract permits real telegram sends")
    if contract.allows_scraping:
        errors.append("Contract permits scraping")
    if contract.allows_dashboard:
        errors.append("Contract permits dashboard")

    return errors

def validate_all_dependency_contracts(contracts: List[DependencyContract]) -> List[str]:
    all_errors = []
    for c in contracts:
        all_errors.extend(validate_dependency_contract_safety(c))
    return all_errors

def dependency_contracts_have_execution_route(contracts: List[DependencyContract]) -> bool:
    return any(c.allows_execution for c in contracts)

def dependency_contracts_have_broker_route(contracts: List[DependencyContract]) -> bool:
    return any(c.allows_broker for c in contracts)

def dependency_contracts_have_order_route(contracts: List[DependencyContract]) -> bool:
    return any(c.allows_order for c in contracts)

def dependency_contracts_have_paper_mutation_route(contracts: List[DependencyContract]) -> bool:
    return any(c.allows_paper_mutation for c in contracts)

def dependency_contract_validator_summary(contracts: List[DependencyContract]) -> Dict[str, Any]:
    errors = validate_all_dependency_contracts(contracts)
    return {
        "is_valid": len(errors) == 0,
        "error_count": len(errors)
    }

def dependency_contract_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "All dependency contracts are valid and safe."
    return f"Validation failed with {len(errors)} errors."
