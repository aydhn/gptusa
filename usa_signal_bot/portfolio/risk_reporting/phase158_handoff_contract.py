from typing import Any, Dict, List
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    Phase158HandoffContract,
    PortfolioBandClosureCertificate,
    PortfolioBandFinalReview,
    create_phase158_handoff_contract_id
)

def build_phase158_handoff_contract(certificate: PortfolioBandClosureCertificate, final_review: PortfolioBandFinalReview) -> Phase158HandoffContract:
    return Phase158HandoffContract(
        contract_id=create_phase158_handoff_contract_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source_certificate_id=certificate.certificate_id,
        source_final_review_id=final_review.review_id,
        read_only=True,
        research_data_only=True,
        integration_handoff_only=True,
        allowed_items=[
            "portfolio_risk_summary",
            "governance_reports",
            "portfolio_band_lineage",
            "closure_certificate"
        ],
        forbidden_fields=[
            "portfolio_weight", "target_weight", "actual_target_weight", "actual_portfolio_weight",
            "allocation", "actual_allocation", "position_size", "actual_position_size", "capital_allocation",
            "order_size", "broker_order", "paper_order", "live_order", "sent_to_broker", "strategy_active",
            "deployment_enabled", "live_signal", "buy_signal", "sell_signal"
        ],
        live_trading_allowed=False,
        paper_trading_allowed=False,
        broker_execution_allowed=False,
        actual_target_weights_allowed=False,
        actual_allocation_allowed=False,
        capital_deployment_allowed=False,
        deployment_allowed=False,
        contract_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_phase158_handoff_contract(contract: Phase158HandoffContract) -> List[str]:
    return []

def phase158_handoff_contract_to_text(contract: Phase158HandoffContract, limit: int = 300) -> str:
    return f"Handoff Contract {contract.contract_id}: valid={contract.contract_valid}"
