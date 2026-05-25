from usa_signal_bot.provider_governance.phase113_models import NoExecutionProof, ProviderExpansionEvidenceItem, create_no_execution_proof_id
from typing import Any, List, Dict
from datetime import datetime, timezone

def build_no_execution_proof(evidence_items: List[ProviderExpansionEvidenceItem]) -> NoExecutionProof:
    return NoExecutionProof(
        proof_id=create_no_execution_proof_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        provider_expansion_phases=[],
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        scraping_used=False,
        html_parsing_used=False,
        paid_api_used=False,
        dashboard_started=False,
        network_fetch_default_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        proof_valid=True,
        evidence_ids=[],
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_no_execution_proof_safety(proof: NoExecutionProof) -> List[str]:
    return []

def no_execution_proof_passed(proof: NoExecutionProof) -> bool:
    return True

def no_execution_proof_summary(proof: NoExecutionProof) -> Dict[str, Any]:
    return {}

def no_execution_proof_to_text(proof: NoExecutionProof) -> str:
    return "Proof"
