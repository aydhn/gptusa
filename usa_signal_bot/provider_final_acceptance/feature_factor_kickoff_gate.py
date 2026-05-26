import hashlib
from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    FeatureFactorEngineKickoffGate,
    FeatureFactorKickoffGateStatus,
    FeatureFactorKickoffGateDecision,
    DataProviderFinalAcceptanceReport,
    ProviderLayerClosureBundle,
    FeatureFactorDataContract,
    FeatureFactorKickoffRuleStatus,
    FeatureFactorKickoffAssertionStatus,
    create_feature_factor_kickoff_gate_id,
    _utc_now
)
from usa_signal_bot.provider_final_acceptance.feature_factor_scope import phase116_allowed_scopes, phase116_blocked_scopes
from usa_signal_bot.provider_final_acceptance.feature_factor_kickoff_rules import build_feature_factor_kickoff_rules
from usa_signal_bot.provider_final_acceptance.feature_factor_kickoff_assertions import build_feature_factor_kickoff_assertions

def build_feature_factor_engine_kickoff_gate(acceptance: DataProviderFinalAcceptanceReport, closure: ProviderLayerClosureBundle, contract: FeatureFactorDataContract) -> FeatureFactorEngineKickoffGate:
    rules = build_feature_factor_kickoff_rules(acceptance, closure, contract)
    assertions = build_feature_factor_kickoff_assertions(acceptance, closure, contract)

    rules_passed = all(r.status == FeatureFactorKickoffRuleStatus.PASS for r in rules)
    assertions_passed = all(a.status == FeatureFactorKickoffAssertionStatus.PASS for a in assertions)

    passed = rules_passed and assertions_passed

    status = FeatureFactorKickoffGateStatus.PASSED_METADATA_ONLY if passed else FeatureFactorKickoffGateStatus.BLOCKED
    decision = FeatureFactorKickoffGateDecision.PASS_TO_PHASE116_FEATURE_FACTOR_ENGINE if passed else FeatureFactorKickoffGateDecision.BLOCK

    return FeatureFactorEngineKickoffGate(
        gate_id=create_feature_factor_kickoff_gate_id(),
        created_at_utc=_utc_now(),
        status=status,
        decision=decision,
        source_acceptance_report_id=acceptance.report_id,
        source_closure_id=closure.closure_id,
        data_contract=contract,
        allowed_scopes=phase116_allowed_scopes(),
        blocked_scopes=phase116_blocked_scopes(),
        rules=rules,
        assertions=assertions,
        gate_hash=stable_feature_factor_kickoff_gate_hash({}),
        sealed=passed,
        immutable=passed,
        frozen=passed,
        metadata_only=True,
        research_data_only=True,
        ready_for_phase116=passed,
        phase116_scope_allowed=passed,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        paid_api_enabled=False,
        dashboard_enabled=False,
        network_default_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def stable_feature_factor_kickoff_gate_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256("gate".encode('utf-8')).hexdigest()

def feature_factor_kickoff_gate_summary(gate: FeatureFactorEngineKickoffGate) -> dict[str, Any]:
    return {
        "status": gate.status,
        "decision": gate.decision,
        "sealed": gate.sealed
    }

def feature_factor_kickoff_gate_to_text(gate: FeatureFactorEngineKickoffGate, limit: int = 300) -> str:
    return f"Kickoff Gate [{gate.status}] - Decision: {gate.decision}, Sealed: {gate.sealed}"
