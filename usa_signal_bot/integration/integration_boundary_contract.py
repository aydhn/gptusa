
from typing import Any, Dict, List

from usa_signal_bot.integration.phase158_models import IntegrationBoundaryContract

def build_integration_boundary_contract() -> IntegrationBoundaryContract:
    contract = IntegrationBoundaryContract()
    contract.contract_valid = len(validate_integration_boundary_contract(contract)) == 0
    return contract

def validate_integration_boundary_contract(contract: IntegrationBoundaryContract) -> List[str]:
    violations = []

    if not contract.read_only_phase158_handoff: violations.append("read_only_phase158_handoff=False")
    if not contract.dry_run_rehearsal_only: violations.append("dry_run_rehearsal_only=False")
    if not contract.local_fixture_only: violations.append("local_fixture_only=False")
    if not contract.no_live_trading: violations.append("no_live_trading=False")
    if not contract.no_paper_state_mutation: violations.append("no_paper_state_mutation=False")
    if not contract.no_broker_execution: violations.append("no_broker_execution=False")
    if not contract.no_real_order_creation: violations.append("no_real_order_creation=False")
    if not contract.no_telegram_real_send: violations.append("no_telegram_real_send=False")
    if not contract.no_strategy_activation: violations.append("no_strategy_activation=False")
    if not contract.no_deployment: violations.append("no_deployment=False")
    if not contract.no_production_patch: violations.append("no_production_patch=False")
    if not contract.no_network: violations.append("no_network=False")
    if not contract.no_scraping: violations.append("no_scraping=False")
    if not contract.no_html_parsing: violations.append("no_html_parsing=False")
    if not contract.no_dashboard: violations.append("no_dashboard=False")
    if not contract.no_daemon: violations.append("no_daemon=False")
    if not contract.no_scheduler: violations.append("no_scheduler=False")
    if not contract.no_actual_target_weights: violations.append("no_actual_target_weights=False")
    if not contract.no_actual_allocation: violations.append("no_actual_allocation=False")
    if not contract.no_order_size: violations.append("no_order_size=False")
    if not contract.no_capital_deployment: violations.append("no_capital_deployment=False")
    if not contract.no_investment_advice: violations.append("no_investment_advice=False")

    return violations

def integration_boundary_contract_to_text(contract: IntegrationBoundaryContract, limit: int = 300) -> str:
    valid = contract.contract_valid
    text = f"Boundary Contract Valid: {valid}"
    return text[:limit] + "..." if len(text) > limit else text
