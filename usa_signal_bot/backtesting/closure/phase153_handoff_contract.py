from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    Phase153HandoffContract, BacktestBandClosureCertificate,
    BacktestFinalAuditReport, Phase153HandoffItemKind, BacktestClosureRiskFlag
)

def build_phase153_handoff_contract(certificate: BacktestBandClosureCertificate, final_audit_report: BacktestFinalAuditReport) -> Phase153HandoffContract:
    contract = Phase153HandoffContract()
    contract.source_certificate_id = certificate.certificate_id
    contract.source_final_audit_report_id = final_audit_report.report_id

    contract.allowed_item_kinds = [
        Phase153HandoffItemKind.READ_ONLY_PERFORMANCE_SUMMARY,
        Phase153HandoffItemKind.READ_ONLY_RISK_SUMMARY,
        Phase153HandoffItemKind.READ_ONLY_ROBUSTNESS_SCORECARD,
        Phase153HandoffItemKind.READ_ONLY_CONSTRAINT_NOTE,
        Phase153HandoffItemKind.READ_ONLY_METRIC_INVENTORY,
        Phase153HandoffItemKind.READ_ONLY_RISK_NOTE_INVENTORY,
        Phase153HandoffItemKind.READ_ONLY_ARTIFACT_LINEAGE,
        Phase153HandoffItemKind.READ_ONLY_SAFETY_SUMMARY,
        Phase153HandoffItemKind.PORTFOLIO_INPUT_CONTRACT
    ]

    contract.forbidden_fields = [
        "portfolio_weight", "target_weight", "allocation", "position_size",
        "capital_allocation", "order", "broker_order", "paper_order", "live_order",
        "sent_to_broker", "strategy_active", "deployment_enabled", "live_signal",
        "buy_signal", "sell_signal"
    ]

    contract.contract_valid = certificate.closed
    if not contract.contract_valid:
        contract.risk_flags.append(BacktestClosureRiskFlag.HANDOFF_CONTRACT_INVALID)
        contract.errors.append("Invalid contract: certificate not closed")

    return contract

def validate_phase153_handoff_contract(contract: Phase153HandoffContract) -> list[str]:
    errors = []
    if not contract.contract_valid:
        errors.append("Contract is invalid")
    if contract.portfolio_construction_allowed:
        errors.append("Portfolio construction must not be allowed in the contract")
    return errors

def phase153_handoff_contract_summary(contract: Phase153HandoffContract) -> dict[str, Any]:
    return {"valid": contract.contract_valid}

def phase153_handoff_contract_to_text(contract: Phase153HandoffContract, limit: int = 300) -> str:
    return f"Phase153HandoffContract(valid={contract.contract_valid})"
