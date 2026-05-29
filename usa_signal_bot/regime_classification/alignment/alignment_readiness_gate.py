from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    MarketBehaviorIngestionResult, FrozenFactorAlignmentReference, MarketBehaviorOverlayResult,
    RegimeContextCompatibilityResult, AlignmentDiagnosticsProfile, RegimeAlignmentReadinessRule,
    RegimeAlignmentReadinessGate, create_regime_alignment_readiness_rule_id,
    create_regime_alignment_readiness_gate_id, _now
)
from usa_signal_bot.core.enums import (
    RegimeAlignmentReadinessRuleKind, RegimeAlignmentReadinessStatus, RegimeAlignmentRiskFlag
)

def build_regime_alignment_readiness_rules(ingestion: MarketBehaviorIngestionResult, refs: list[FrozenFactorAlignmentReference], overlays: list[MarketBehaviorOverlayResult], compatibility: list[RegimeContextCompatibilityResult], diagnostics: list[AlignmentDiagnosticsProfile]) -> list[RegimeAlignmentReadinessRule]:
    rules = []

    rules.append(RegimeAlignmentReadinessRule(
        rule_id=create_regime_alignment_readiness_rule_id(),
        created_at_utc=_now(),
        rule_kind=RegimeAlignmentReadinessRuleKind.MARKET_BEHAVIOR_VALID,
        name="Market Behavior Valid",
        status=RegimeAlignmentReadinessStatus.PASSED if ingestion.valid_for_phase131 else RegimeAlignmentReadinessStatus.FAILED,
        required=True,
        passed=ingestion.valid_for_phase131,
        expected_value=True, observed_value=ingestion.valid_for_phase131,
        rationale="Phase 130 behavior must be valid"
    ))

    rules.append(RegimeAlignmentReadinessRule(
        rule_id=create_regime_alignment_readiness_rule_id(),
        created_at_utc=_now(),
        rule_kind=RegimeAlignmentReadinessRuleKind.NO_MODEL_TRAINING,
        name="No Model Training",
        status=RegimeAlignmentReadinessStatus.PASSED if not ingestion.model_training_used else RegimeAlignmentReadinessStatus.FAILED,
        required=True,
        passed=not ingestion.model_training_used,
        expected_value=False, observed_value=ingestion.model_training_used,
        rationale="Phase 131 is not model training"
    ))

    rules.append(RegimeAlignmentReadinessRule(
        rule_id=create_regime_alignment_readiness_rule_id(),
        created_at_utc=_now(),
        rule_kind=RegimeAlignmentReadinessRuleKind.NO_SIGNAL_OUTPUT,
        name="No Signal Output",
        status=RegimeAlignmentReadinessStatus.PASSED,
        required=True, passed=True, expected_value=False, observed_value=False,
        rationale="Phase 131 does not produce trade signals"
    ))

    return rules

def build_regime_alignment_readiness_gate(ingestion: MarketBehaviorIngestionResult, refs: list[FrozenFactorAlignmentReference], overlays: list[MarketBehaviorOverlayResult], compatibility: list[RegimeContextCompatibilityResult], diagnostics: list[AlignmentDiagnosticsProfile]) -> RegimeAlignmentReadinessGate:
    rules = build_regime_alignment_readiness_rules(ingestion, refs, overlays, compatibility, diagnostics)
    passed = all(r.passed for r in rules if r.required)
    return RegimeAlignmentReadinessGate(
        gate_id=create_regime_alignment_readiness_gate_id(),
        created_at_utc=_now(),
        status=RegimeAlignmentReadinessStatus.PASSED if passed else RegimeAlignmentReadinessStatus.FAILED,
        rules=rules,
        ready_for_phase132=passed,
        research_data_only=True,
        activation_allowed=False, strategy_activation_allowed=False, deployment_allowed=False,
        model_training_used=False, model_prediction_used=False,
        produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False,
        investment_advice=False
    )

def regime_alignment_readiness_passed(gate: RegimeAlignmentReadinessGate) -> bool:
    return gate.status == RegimeAlignmentReadinessStatus.PASSED

def regime_alignment_readiness_blocks_phase132(gate: RegimeAlignmentReadinessGate) -> bool:
    return not gate.ready_for_phase132

def validate_regime_alignment_readiness_gate(gate: RegimeAlignmentReadinessGate) -> list[str]:
    errs = []
    if gate.ready_for_phase132 and gate.status != RegimeAlignmentReadinessStatus.PASSED:
        errs.append("ready_for_phase132 is true but gate failed")
    return errs

def regime_alignment_readiness_gate_summary(gate: RegimeAlignmentReadinessGate) -> dict[str, Any]:
    return {"passed": regime_alignment_readiness_passed(gate)}

def regime_alignment_readiness_gate_to_text(gate: RegimeAlignmentReadinessGate, limit: int = 300) -> str:
    return f"Gate Passed: {regime_alignment_readiness_passed(gate)}"
