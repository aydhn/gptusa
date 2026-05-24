from typing import Dict, Any, List
import hashlib
import json
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    DataProviderExpansionKickoffGate,
    DataProviderExpansionKickoffGateStatus,
    DataProviderExpansionKickoffGateDecision,
    CoreRuntimeAcceptanceReport,
    AdvancedFoundationFreezeBundle,
    ProviderKickoffRule,
    ProviderKickoffAssertion,
    CoreRuntimeAcceptanceRiskFlag,
    create_data_provider_kickoff_gate_id,
    _now
)

def build_data_provider_expansion_kickoff_gate(acceptance_report: CoreRuntimeAcceptanceReport, foundation_freeze: AdvancedFoundationFreezeBundle) -> DataProviderExpansionKickoffGate:
    gate = build_default_data_provider_expansion_kickoff_gate()
    gate.source_acceptance_report_id = acceptance_report.report_id
    gate.source_foundation_freeze_id = foundation_freeze.freeze_id
    gate.acceptance_report = acceptance_report
    gate.foundation_freeze = foundation_freeze

    status = DataProviderExpansionKickoffGateStatus.PASSED_METADATA_ONLY if acceptance_report.core_runtime_accepted and foundation_freeze.frozen else DataProviderExpansionKickoffGateStatus.BLOCKED
    decision = DataProviderExpansionKickoffGateDecision.PASS_TO_PHASE106_DATA_PROVIDER_EXPANSION if status.name == "PASSED_METADATA_ONLY" else DataProviderExpansionKickoffGateDecision.BLOCK

    gate.status = status
    gate.decision = decision
    gate.gate_hash = stable_provider_kickoff_gate_hash({"status": status.name})
    return gate

def build_default_data_provider_expansion_kickoff_gate() -> DataProviderExpansionKickoffGate:
    return DataProviderExpansionKickoffGate(
        gate_id=create_data_provider_kickoff_gate_id(),
        created_at_utc=_now(),
        status=DataProviderExpansionKickoffGateStatus.CREATED,
        decision=DataProviderExpansionKickoffGateDecision.UNKNOWN,
        sealed=True,
        immutable=True,
        frozen=True,
        metadata_only=True,
        provider_ready=True,
        ready_for_phase106=True,
        phase106_scope_allowed=True,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        dashboard_enabled=False,
        paid_api_enabled=False,
        provider_network_fetch_required=False,
        execution_performed=False,
        network_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        scraping_used=False,
        dashboard_started=False
    )

def stable_provider_kickoff_gate_hash(payload: Dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def collect_provider_kickoff_risk_flags(rules: List[ProviderKickoffRule], assertions: List[ProviderKickoffAssertion]) -> List[CoreRuntimeAcceptanceRiskFlag]:
    return []

def provider_kickoff_gate_summary(gate: DataProviderExpansionKickoffGate) -> Dict[str, Any]:
    return {
        "status": gate.status.name,
        "ready": gate.ready_for_phase106
    }

def provider_kickoff_gate_to_text(gate: DataProviderExpansionKickoffGate, limit: int = 200) -> str:
    return f"Kickoff Gate: {gate.status.name}"
